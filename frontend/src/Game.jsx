import Board from './Board'
import ClueBoard from './ClueBoard'
import React, { useState, useEffect} from 'react';
import './index.css'

function Game(){

    //Default dimension is 5
    const [dim, setDim] = useState(5);
    const [board, setBoard] = useState([]);
    const [horizontal, setHorizontal] = useState({});
    const [vertical, setVertical] = useState({});

    const onDimChange = (e) => {
        setDim(e.target.value);
        //console.log(dim);
    }


    // API stuff
    
    const fetchData = () => {
        // Temporarily hardcode 2
        fetch('http://127.0.0.1:8000/2')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                //setPosts(data);
                setBoard(data.board);
                setHorizontal(data.horizontal);
                setVertical(data.vertical);
            })
            .catch((error) => {
                console.error('Fetch error:', error);
            });
    };
    

    return(
        <>
        <button onClick={fetchData}>Fetch Data</button> {/* Add this button */}
        <Board dimension={dim}/>
        <div className="dim-input">
            <input type="number" value={dim} onChange={onDimChange}></input>
        </div>
        <div className="dim-label">
            <ClueBoard horizontal={horizontal} vertical={vertical}/>
        </div>
        </>
    )
}

export default Game