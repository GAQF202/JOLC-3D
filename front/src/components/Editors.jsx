import '../App.css';
//import MyEditor from './componentes/MyEditor';
import Editor from "@monaco-editor/react";
import React from 'react'

function Editors({archivo, onChange, visible, handleEditorDidMount}) {
    return (
        <div className="todo">

            <div className="entrada" style={{display:visible?"block":"none"}}>
                <Editor
                    height="80vh"
                    width="90vh"
                    theme="vs-dark"
                    onMount={handleEditorDidMount}
                    onChange = {onChange}
                    value = {archivo||""}
                />
            </div>
      </div>
        
    ); 
}


export default Editors;