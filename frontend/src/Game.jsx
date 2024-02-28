import Board from './Board'
import React, { useState } from 'react';

function Game(){

    //Default dimension is 3
    const [dim, setDim] = useState(3);

    const onDimChange = (e) => {
        setDim(e.target.value);
        //console.log(dim);
    }


    return(
        <>
        <Board dimension={dim}/>
        <div className="dim-input">
            <input type="number" value={dim} onChange={onDimChange}></input>
        </div>
        </>
    )
}

export default Game