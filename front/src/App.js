import './App.css';
import React, { useRef } from 'react'
import {BrowserRouter, Switch, Route} from 'react-router-dom'
import Principal from './components/Principal';
import Arbol from './components/Arbol';
import Errores from './components/Errores';
import TS from './components/TS';
import Bienvenida from './components/Bienvenida';
import Nav from './components/Nav';
//import Hola from './components/Hola';
//<Route exact path='/ver' component={Hola}/>

function App() {

   
  //console.log(editores)
  return (
    <div>

      <BrowserRouter>
        <div className="div-nav">
          <Nav/>
        </div>
        <Switch>
          <Route exact path='/' component={Principal}/>
          <Route exact path='/index' component={Bienvenida}/>
          <Route exact path='/arbol' component={Arbol}/>
          <Route exact path='/ts' component={TS}/>
          <Route exact path='/errores' component={Errores}/>
        </Switch>
      </BrowserRouter>
     
    </div>
  );
}

export default App;
