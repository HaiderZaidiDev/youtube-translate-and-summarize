import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import VideoIcon from './video-icon.svg'

const Header = () => {
    return (
        <Row className="header">
            <Col xs={12} md={6}>
                <h1> Translate and Summarize Youtube Videos</h1>
                <p> YouTube videos can be long and difficult to watch - many don’t have captions and are in varying languages. In an effort to make the world smaller and increase accessibility of information, this platform can translate and summarize videos for you.</p>
                <button type="text" className="btn-cta"> <a href="https://github.com/HaiderZaidiDev/youtube-translate-and-summarize" target="_blank">See the Code</a></button>
            </Col>
            <Col xs={6} className="header-icon" className="d-none d-md-block">
                <img src={VideoIcon}/><img/>
            </Col>
        </Row>
    )
}

export default Header
