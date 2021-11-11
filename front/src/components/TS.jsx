import React, {  useState } from "react";
import {useEffect} from 'react'

//fetch("http://localhost:4000/ts",{method:"GET"})
const TS = () => {
    const [data,setData] = useState(null)
    useEffect(()=>{
        fetch("https://ihateyouheroku.herokuapp.com/ts",{method:"GET"})
        .then((data)=>data.json())
        .then((json)=>{setData(json)})
    },[])
    console.log(data)
    return(
        <div id="main-container">
            <table>
                <tr>
                    <th>Identificador</th>
                    <th>Tipo</th>
                    <th>Entorno</th>
                    <th>Linea</th>
                    <th>Columna</th>
                </tr>
                {
                    data?.map( simbolo=>(
                        <tr>
                            <td>{simbolo.nombre}</td>
                            <td>{simbolo.tipo}</td>
                            <td>{simbolo.ambito}</td>
                            <td>{simbolo.fila}</td>
                            <td>{simbolo.columna}</td>
                        </tr>
                        )
                    )
                }
            </table>

        </div>
    )
}

export default TS