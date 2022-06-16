import './App.css';

/* Bootstrap Components */
import Container from 'react-bootstrap/Container'

/* Core Components */
import Header from './components/Header.js'
import Midbar from './components/Midbar.js'

const App = () => {
  return (
    <Container fluid>
      <Header/>
      <Midbar/>
    </Container>
  );
}



export default App;
