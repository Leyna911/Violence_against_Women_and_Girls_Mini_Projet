import './App.css';
import MapTitle from './Components/MapTitle';
import {BrowserRouter, Route, Routes} from "react-router-dom"


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<MapTitle/>}/>
      </Routes> 
    </BrowserRouter>
    
  );
}

{/*  */}



export default App;
