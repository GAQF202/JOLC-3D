import '../App.css';
//import MyEditor from './componentes/MyEditor';
import Editor from "@monaco-editor/react";
//import React, { useState } from 'react';
import React, { useRef } from 'react'
import {  useState } from "react";
import Editors from '../components/Editors';
import Nav from '../components/Nav';

import { useHistory } from "react-router-dom";

function Principal() {

    const [editores,setEditores] = useState(["Editor0"])
    const history = useHistory()

    const options = {
        readOnly: true
    };
  
    const editorRef = useRef(null);
  
    function handleEditorDidMount(editor, monaco) {
      editorRef.current = editor; 
    }
    const [salida,setSalida] = useState("")
    //ACTIVO
    const [seleccionado,setSeleccionado] = useState(0)
  
    const [cher,setCher] = useState([""])
  
    function setContenido(valor){
        setCher((chers)=>{
          let copiaChers = [...chers]
          copiaChers[seleccionado] = valor
          return copiaChers
        })
    }

    function showValue() {
        //window.location.reload(false);
        //fetch('http://localhost:4000/correr'
        fetch('https://ihateyouheroku.herokuapp.com/correr', {
        //fetch('http://localhost:5000/correr', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            'prueba' : cher[seleccionado],
          })
        })
        .then((datos)=>datos.json())
        .then((json)=>{setSalida(json)})
        //window.location.reload(false)
        //console.log("aquii",cher[seleccionado])
        console.log("Estoo",salida.output)
      }

      function agregarEditor(){
        //window.location.reload(false);
        setEditores((editores2)=>{
          const editores1 = [...editores2]
          editores1.push("Editor"+(editores1.length))
          setSeleccionado(editores1.length-1)
          return editores1
        })
      }
    
      function quitarEditor(){
        //window.location.reload(false);
        setEditores((editores2)=>{
          const editores1 = [...editores2]
          editores1.pop()
          return editores1
        })
        setCher((archivo2)=>{
            const archivo1 = [...archivo2]
            archivo1.pop()
            setSeleccionado(archivo1.length)
            return archivo1
          })
        
      }
      
      function seleccionarEditor(numero){
        //window.location.reload(false);
        return function(){
          setSeleccionado(numero)
        }
      }

      function abrir(event){
        const input = event.target
        const reader = new FileReader()
        console.log(input.files)
        reader.onload = () =>{
            let data = reader.result
            //let ruta = reader.path
            setCher((chers)=>{
              let copia = Array(editores.length).fill("").map((_l,index)=>{
                  if(chers[index] && chers[index].length>0)return chers[index]
                  else return ""
              })
              copia[seleccionado] = data
              return copia;
            });
            setRutasChers((chers)=>{
              let copia = Array(editores.length).fill("").map((_l,index)=>{
                  if(chers[index] && chers[index].length>0)return chers[index]
                  else return ""
              })
              copia[seleccionado] = data
              return copia;
            });
        }
        reader.readAsText(input.files[0])
    }
    const [rutasChers,setRutasChers] = useState([""])
    function guardar(){
      fetch('http://localhost:3000/guardar', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            'prueba' : cher[seleccionado]
          })
        })
    }

    //console.log(editores)
    return (
        <div>
        <button type="button" onClick={showValue} id="boton-compilar"><b>Compilar</b><img src="./compilar.png"></img> </button>
        <div className="menu">
        <input id="abrir" style={{display:'none'}} onChange={abrir} type="file"/>
          <button onClick={agregarEditor}>Nuevo</button>
          <button onClick={quitarEditor}>Quitar</button>
        </div>
        <div className="lista-botones">
          {editores?.map((editor,index)=>{
              return         <div className="selectores">
                      <button onClick={seleccionarEditor(index)}>{editor}</button>
                  </div>
          })}
        </div>
        {editores?.map((editor,index)=>{
          return <Editors archivo={cher[index]} onChange={setContenido} visible={index===seleccionado} key={editor} handleEditorDidMount={handleEditorDidMount} />
        })}
        <div className="consol">
            <Editor
            options={options}
              height="80vh"
              width="90vh"
              //defaultLanguage="javascript"
              theme="vs-dark"
              readOnly = 'true'
              value = {salida.output}
              //onMount={handleEditorDidMount2}
            />
        </div>
  
      </div>
    );
}

export default Principal;
