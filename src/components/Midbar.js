import React, {useState, useEffect} from "react";
import axios from "axios"

/* Bootstrap Components */
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner'


/* Core Components */
import VideoResults from './VideoResults.js'

const Midbar = () => {
    const [youtubeLink, setYoutubeLink] = useState('')
    const [language, setLanguage] = useState('english')
    const [videoMeta, setVideoMeta] = useState('')
    const [transcription, setTranscription] = useState('')
    const [summary, setSummary] = useState('')
    const [translation, setTranslation] = useState('')
    const [loading, setLoadingStatus] = useState(false)

    useEffect(() => {
        /* Once the video has been downloaded on the backend and the meta data is retrieved. */
        // Transcribing the video.
        if (videoMeta) {
            console.log('Transcribing...')
            axios.get(`/api/transcribe?id=${videoMeta.id+videoMeta.ext}`)
            .then((res) => {
                var transcription = res.data.text
                setTranscription(transcription)
                console.log(transcription)
            })
            .catch((err) => {
                console.log(`Error: ${err}`)
            })
        }



        // Summarizing the transcription.
        if (transcription) {
            console.log('Summarizing...')
            axios.get(`/api/summary?text=${transcription}`)
            .then((res) => {
                var summary = res.data
                setSummary(summary)
                console.log(summary)

            })
            .catch((err) => {
                console.log(`Error: ${err}`)
            })
        }

        // Translating the transcription.

        if (transcription) {
            console.log('Translating...')
            axios.get(`/api/translate?text=${transcription}&lang=${language}`)
            .then((res) => {
                var translation= res.data
                setTranslation(translation)
                console.log(translation)
                setLoadingStatus(false)

            })
            .catch((err) => {
                console.log(`Error: ${err}`)
            })
        }


    }, [videoMeta, transcription, summary, translation])

    const LoadingIcon = () => {
        return (
            <Row className="loading-icon">
                <Spinner animation="border" role="status" style={{color:'#5E548E'}}>
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            </Row>
        );
    }
    const fetchResponse = () => {
        /* Downloading the video on the back-end server, fetching the video's meta data used for further operations. */
        axios.get(`/api/download?url=${youtubeLink}`)
        .then((res) => {
            let meta = {
                id: res.data.video_id,
                ext: res.data.ext,
            }
            setVideoMeta(meta)

        })
        .catch((err) => {
            console.log(`Error: ${err}`)
        })

    }

    const submitHandler = (event) => {
        /* Handling form submission */

        event.preventDefault();
        setLoadingStatus(true) // Updating loading status.
        fetchResponse()
    }
    return (
        <React.Fragment>
            <Row className="midbar">
                <Col xs={12}>
                    <div className="midbar-header">
                        <Row>
                            <h2> How it Works </h2>
                            <p> Paste a YouTube video link and we'll transcribe, summarize, and translate it to a language of your choice.</p> 
                        </Row>
                    </div>
                    <div className="youtube-input-wrapper">
                        <Row>
                            <form onSubmit={submitHandler}>
                                <input 
                                    type='text' 
                                    placeholder="https://youtube.com/watch?="
                                    className="youtube-input"
                                    onChange = {(event) => setYoutubeLink(event.target.value)}
                                    >
                                </input>
                                <label htmlFor="language"> </label>
                                <select name="language" id="language" className="dropdown" onChange={(event) => setLanguage(event.target.value)}>
                                    <option value="english">English</option>
                                    <option value="french">French</option>
                                </select> 
                                <button type="submit" className="submit-btn"> Submit </button>
                            </form>
                        </Row>
                    </div>
                </Col>
            </Row>
            {!loading 
            ? <VideoResults summary={summary} translation={translation}/>
            : <LoadingIcon/>
            }

        </React.Fragment>


    )
}

export default Midbar
