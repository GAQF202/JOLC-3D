import './components.css';
import React from 'react'
import { Link } from "react-router-dom";

const Nav = () => {
    return(
        <div>
            <ul className="menu-nav">
                <li>
                    <Link className='li-link' to='/index' >Inicio</Link>
                </li>
                <li>
                    <Link className='li-link' to='/' >Compilador</Link>
                </li>
                <li>
                    <Link className='li-link' to='/arbol' >CST</Link>
                </li>
                <li>
                    <Link className='li-link' to='/ts' >TS</Link>
                </li>
                <li>
                    <Link className='li-link' to='/errores' >Errores</Link>
                </li>
            </ul>
        </div>
    )
}

export default Nav