import Cell from './Cell'
import React, { useState, useEffect} from 'react';



function Board({dimension}) {
    //Need array to keep track of board
    dimension = Number(dimension);
    // Create an innerArray for each row, so each row is fresh array
    const createRow = () => Array(dimension).fill(null);
    // Initialize the 2D array with above rows, each filled with null values initially
    const [squares, setSquares] = useState(Array.from({ length: dimension }, createRow));

    //Updates the dimensions when the dimension is changed
    useEffect(() => {
        // This effect will run whenever the `dimension` prop changes
        setSquares(Array.from({ length: dimension }, createRow));
    }, [dimension]); // Adding `dimension` to the dependency array

    // To be used to check if a row or column is correct
    useEffect(() => {
        // This function will run after `squares` has been updated
        printSquares();




        
      }, [squares]); // Dependency array, useEffect runs when `squares` changes
      


    // Function to update the squares
    const handleCellFill = (rowIndex, cellIndex, value) => {
        // Create a new array with the same values as the current squares
        const newSquares = [...squares];
        // Create a new row with the same values as the current row
        const newRow = [...newSquares[rowIndex]];
        // Change the value of the cell
        newRow[cellIndex] = value;
        // Change the value of the row
        newSquares[rowIndex] = newRow;
        // Update the state with the new array
        console.log(`${rowIndex} ${cellIndex} ${value}`)
        setSquares(newSquares);
    }

    useEffect(() => {
  // This function will run after `squares` has been updated
  printSquares();
}, [squares]); // Dependency array, useEffect runs when `squares` changes

    

    

    // Update the dimension to the board
    // NOte that you need a wrapper function since otherwise you would directly call handle cell fille
    const renderCell = (cell, rowIndex, cellIndex) => (
        <td className="board-item" key={cellIndex}>
          <Cell value={cell} onCellFill={(value) => handleCellFill(rowIndex, cellIndex, value)} />
        </td>
      );
    
    const renderRow = (row, rowIndex) => (
    <tr className="board-row" key={rowIndex}>
        {row.map((cell, cellIndex) => renderCell(cell, rowIndex, cellIndex))}
    </tr>
    );

    // New function to render all rows
    const renderBoard = () => squares.map((row, rowIndex) => renderRow(row, rowIndex));
    

    // Helper Functions
    const printSquares = () => {
        squares.forEach((row, rowIndex) => {
            console.log(`Row ${rowIndex}:`, row.join(', '));
        });
          
    }

    //Pass the state and the function to change state down to the cell
    return(
    <table className="board"> 
        <tbody>
            {renderBoard()}  
        </tbody>
    </table>
    );
}

export default Board
