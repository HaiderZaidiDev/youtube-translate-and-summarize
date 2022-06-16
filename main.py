from youtube_transcript_api import YouTubeTranscriptApi as YTA
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import subprocess
from ibm_watson.websocket import RecognizeCallback, AudioSource
import ffmpeg
import sys
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from moviepy.editor import VideoFileClip
import youtube_dl
import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import language_tool_python    
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

def grammar(text):                                                                                         
    tool = language_tool_python.LanguageTool('en-US')                                                  
                                                                                                       
    matches = tool.check(text)                                                                         
                                                                                                       
    my_mistakes = []                                                                                   
    my_corrections = []                                                                                
    start_positions = []                                                                               
    end_positions = []                                                                                 
                                                                                                       
    for rules in matches:                                                                              
     if len(rules.replacements) > 0:                                                                   
         start_positions.append(rules.offset)                                                          
         end_positions.append(rules.errorLength + rules.offset)                                        
         my_mistakes.append(text[rules.offset:rules.errorLength + rules.offset])                       
         my_corrections.append(rules.replacements[0])                                                  
                                                                                                       
    my_new_text = list(text)                                                                           
                                                                                                       
    for m in range(len(start_positions)):                                                              
     for i in range(len(text)):                                                                        
         my_new_text[start_positions[m]] = my_corrections[m]                                           
         if start_positions[m] < i < end_positions[m]:                                                 
             my_new_text[i] = ""                                                                       
                                                                                                       
    my_new_text = "".join(my_new_text)                                                                 
    return(tool.correct(text))                                                                          
      
raw = input("Please enter your youtube video url: ")

def dl(url):                                                                                                            
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'format': 'bestaudio/best','postprocessors': [{   
        'key': 'FFmpegExtractAudio',                                                                                 
        'preferredcodec': 'wav',                                                                                     
        'preferredquality': '192',                                                                                   
    }]})                                                                                                             
                                                                                                                     
    with ydl:                                                                                                        
        result = ydl.extract_info(url, download=True)                                                                
    if 'entries' in result:                                                                                          
        audio_file = result['entries'][0]                                                                            
    else:                                                                                                            
        audio_file = result                                                                                          
                                                                                                              
dl(raw)
rawsplit = raw.rsplit("=", 1)[1]

r = sr.Recognizer()
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


audio = rawsplit + '.wav'
transcript = get_large_audio_transcription(audio)



def summry(text):
    API_KEY = "AD22A4D932"
    API_ENDPOINT = "https://api.smmry.com"
    data = {"sm_api_input": text}
    params = {"SM_API_KEY": API_KEY, "SM_IGNORE_LENGTH": True, "SM_QUESTION_AVOID": True}
    header_params = {"Expect": "100-continue"}
    r = requests.post(url=API_ENDPOINT, params=params, data=data, headers=header_params)
    json_dict = r.json()
    return json_dict['sm_api_content']

final = summry(transcript)



def translate(text):
    translated = GoogleTranslator(source='auto', target='fr').translate(summry(text))
    return translated

final_t = translate(transcript)

print(final)
print("---------------------------------------------------------")
print("---------------------------------------------------------")
print("---------------------------------------------------------")
<<<<<<< HEAD
print(final_t)
=======
print(final_t)
>>>>>>> 31c34bdcf70eabc05ff8dc55cb8a62e012ec69e8
