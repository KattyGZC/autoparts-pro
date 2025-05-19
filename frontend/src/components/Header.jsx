import { useNavigate } from "react-router-dom";

const Header = ({ title }) => {
  const navigate = useNavigate();

  return (
    <div className="header-container">
      <button className="back-button" onClick={() => navigate(-1)}>
        ⬅
      </button>
      <h1>{title}</h1>
    </div>
  );
};

export default Header;
