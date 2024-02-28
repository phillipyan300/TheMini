

function Clues({clues}) {

    return(
         
            <div>
                <ul className="no-bullets">
                    {Object.entries(clues).map(([key, value]) => (
                        <li key={key}>{key}: {value}</li>
                    ))}
                </ul>
            </div>
        
        )
}

export default Clues
