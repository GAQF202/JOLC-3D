import React, {  useState } from "react";
import {useEffect} from 'react'

//<img src="http://localhost:4000/static/images/Tree.svg"/>
const Arbol = () => {
    const [data,setData] = useState(null)
    useEffect(()=>{
        fetch("https://ihateyouheroku.herokuapp.com/arbol",{method:"GET"})
        .then((data)=>data.text())
        .then((json)=>{setData(json)})
    },[])
    console.log(data)
    return(
        <div className="div-arbol">
            <span dangerouslySetInnerHTML= {{__html:data}} />
        </div>
    )
}

export default Arbol