import { useNavigate } from 'react-router-dom';


function Start() {
    const navigate = useNavigate();

    const goToAnotherPage = () => {
    navigate('/game');
    };

    return <button className="button" onClick={goToAnotherPage}>Play Game</button>;
}
  
export default Start