import React, {  useState } from "react";
import {useEffect} from 'react'
//fetch("http://localhost:4000/error",{method:"GET"})
const Errores = () => {
    const [data,setData] = useState(null)
    useEffect(()=>{
        fetch("https://ihateyouheroku.herokuapp.com/error",{method:"GET"})
        .then((data)=>data.json())
        .then((json)=>{setData(json)})
    },[])
    console.log(data)
    return(
    <div id="main-container">
        <table>
            <tr>
                <th>No.</th>
                <th>Descripción</th>
                <th>Linea</th>
                <th>Columna</th>
                <th>Fecha y hora</th>
            </tr>
            {
                data?.map( (simbolo,index)=>(
                    <tr>
                        <td>{index}</td>
                        <td>{simbolo.descripcion}</td>
                        <td>{simbolo.fila}</td>
                        <td>{simbolo.columna}</td>
                        <td>{simbolo.date}</td>
                    </tr>
                    )
                )
            }
        </table>

    </div>
    )
}

export default Errores