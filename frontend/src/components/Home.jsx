import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home-container">
      <h1>AutoPartsPro Dashboard</h1>
      <div className="home-navigation">
        <Link to="/customers" className="home-button" style={{ backgroundColor: '#3F8E41' }}>
          Customers
        </Link>
        <Link to="/vehicles" className="home-button" style={{ backgroundColor: '#1B7AC5' }}>
          Vehicles
        </Link>
        <Link to="/inventory" className="home-button" style={{ backgroundColor: '#7F208F' }}>
          Inventory
        </Link>
        <Link to="/repair-orders" className="home-button" style={{ backgroundColor: '#E68801' }}>
          Repair Orders
        </Link>
      </div>
      <div className="home-content">
      </div>
    </div>
  );
};

export default Home;
