import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


const Result = (props) => {
    return (
        <Col xs={12}>
            <h2>Video Summary & Translation</h2>
            <div className="result-box">
                <div className="result-item">
                    <Row className="result-row">
                        <Col xs={3}>
                            <p> <strong>Summary</strong></p>
                        </Col>
                        <Col xs={9}>
                            <p> {props.summary} </p>
                        </Col>
                    </Row>
                    <Row className="result-row">
                        <Col xs={3}>
                            <p> <strong> Translation </strong></p>
                        </Col>
                        <Col xs={9}>
                            <p> {props.translation} </p>
                        </Col>
                    </Row>
                </div>
            </div>
        </Col>
    )
}

const VideoResults = (props) => {
    /* props:

    summary: str 
        Summary of the video.
    
    translation: str 
        Translation version of the video
    */
    return (
        <Row className="results">
            <Result summary={props.summary} translation={props.translation}/>
        </Row>
    )
}


export default VideoResults