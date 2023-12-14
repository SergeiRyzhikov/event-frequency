import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './pages/Login';
import Verify from './pages/Verify';
import Main from './pages/Main';
import History from './pages/History';
import './styles/App.css'

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path='/login' element={<Login/>}/>
      <Route path='/verify' element={<Verify/>}/>
      <Route path='/' element={<Main/>}/>
      <Route path='/history' element={<History/>}/>
    </Routes>
    </BrowserRouter>
  );
}

export default App;
