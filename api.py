import requests
import os
from flask import Flask, request, render_template
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pytube import YouTube
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
app = Flask(__name__, static_folder='build/static', template_folder="build")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/download', methods=["GET"])
def download():
    """Downloads a YouTube file as an MP3.

    Notes
    -----
    API URL Format: link.com/api/download?url=
    """
    url = request.args.get('url')
    video_id = url.rsplit("=", 1)[1]

    # Downloading audio only YouTube video, still an MP4.
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video_file = video.download(output_path='/var/www/gettranscript.ca/OHM/videos')

    # Converting video file to an MP3
    audio_file = f"/var/www/gettranscript.ca/OHM/videos/{video_id}.aac"
    os.rename(video_file, audio_file)
    return {
        "video_id":video_id,
        "ext": '.aac'
    }

@app.route('/api/transcribe', methods=["GET"])
def transcribe():
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks

    Notes
    -----
    API URL Format: link.com/api/transcribe?id=

    """
    id = request.args.get('id') # Location of the MP3 file.
    path = f"/var/www/gettranscript.ca/OHM/videos/{id}"

    # Open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "/var/www/gettranscript.ca/OHM/audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.aac")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        r = sr.Recognizer()
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
    # return the text for all chunks detected
    return {'text':whole_text}


@app.route('/api/summary', methods=["GET", "POST"])

def summary() -> dict:
    """
    Fetches a summary of a text.

    Returns
    -------
    dict: JSON response containing the summary of a given text.

    Notes
    -----
    API URL Format: link.com/api/summary?text=
    """
    # Fetching the text from the query URL.

    api_key = os.environ['SMMRY_API_KEY']
    api_endpoint = "https://api.smmry.com"
    text = request.args.get('text')

    # Building Payload
    data = {"sm_api_input": text}
    params = {"SM_API_KEY": api_key, "SM_IGNORE_LENGTH": True, "SM_QUESTION_AVOID": True}

    header_params = {"Expect": "100-continue"}
    r = requests.post(url=api_endpoint, params=params, data=data, headers=header_params)
    json_dict = r.json()

    return json_dict['sm_api_content']

@app.route('/api/translate', methods=['GET'])
def translate() -> str:
    """

    Returns
    -------
    translated_text: str
        Translated version of the summarized text.

    Notes
    -----
    API URL Format: link.com/api/translate?text=&lang=
    """
    lang= request.args.get('lang')
    summarized_text = request.args.get('text')
     
    s = summarized_text
    o = []
    while s:
      o.append(s[:4999])
      s = s[4999:]
 
    translated_text = GoogleTranslator(source='auto', target=lang).translate_batch(o)
    return translated_text
