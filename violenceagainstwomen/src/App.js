import './App.css';
import Map from './Components/map';


function App() {
  return (
    <div className='flex flex-col items-center justify-center ' >
      <div>
            <h1 className=''>This Map represents the world map</h1>
        </div>
      <Map/>
    </div>
  );
}

export default App;
