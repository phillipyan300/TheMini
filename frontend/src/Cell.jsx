

function Cell({value, onCellFill}) {


    const checkChar = (event) => {
        //console.log(event)
        // Entered value
        console.log(event.target.value)
        // Only allow letters
        const character = event.target.value.replace(/\W|\d/g, '').substr(0, 1).toUpperCase();
        event.target.value = character;

        // Call parent function to update
        onCellFill(event.target.value);
    }

    return(<input className="cell" maxLength="1" onKeyUp={checkChar}></input>)
}

export default Cell
