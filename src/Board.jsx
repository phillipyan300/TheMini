import Cell from './Cell'


function Board() {

    return(<table className="board"> 
    <tr className="board-row">
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
    </tr>
    <tr className="board-row">
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
    </tr>
    <tr className="board-row">
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
      <td className="board-item"><Cell/></td>
    </tr>
  </table>)
}

export default Board
