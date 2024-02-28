import Clue from './Clues'
import './index.css'

function ClueBoard({ horizontal, vertical }) {
    return(
        <>
            <table className="clue-board"> 
                <tbody>
                    <tr>
                        <td>
                            {/* Pass horizontal clues to the first Clue component */}
                            <Clue clues={horizontal} />
                        </td>
                        <td>
                            {/* Pass vertical clues to the second Clue component */}
                            <Clue clues={vertical} />
                        </td>
                    </tr>
                </tbody>
            </table>
        </>
    );
}

export default ClueBoard;
