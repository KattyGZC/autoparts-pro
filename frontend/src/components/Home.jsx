import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getOptimizedOrders, updateOrderStatus } from "../services/repairOrderApi";

const Home = () => {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleUpdateOrderStatus = async (orderId, status) => {
    try {
      const response = await updateOrderStatus(orderId, status);
      if (response) {
        navigate(`/repair-orders/detail/${orderId}`);
      } else {
        alert('Failed to update repair order status. Please try again.');
      }
    } catch (error) {
      console.error('Error updating repair order status:', error);
      alert('Failed to update repair order status. Please try again.');
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getOptimizedOrders();
      setOrders(data);
      setLoading(false);
    };

    fetchData();
  }, []);
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
        <h2>Recent Repair Orders</h2>
        {loading ? (
          <p>Loading orders...</p>
        ) : (
          <table className="short-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Vehicle</th>
                <th>Total Cost</th>
                <th>Expected Profit</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr
                  key={order.repair_order_id}
                  className={`repair-order-row${order.status === 'completed' || order.status === 'cancelled' ? ' is-completed' : ''}`}
                >
                  <td>{order.repair_order_id}</td>
                  <td>{order.customer?.name || 'N/A'}</td>
                  <td>{order.vehicle?.license_plate || 'N/A'}</td>
                  <td>${order.total_cost_repair.toFixed(2)}</td>
                  <td>${order.expected_profit.toFixed(2)}</td>
                  <td>
                    <button
                      className="button button--success badge"
                      onClick={() => handleUpdateOrderStatus(order.repair_order_id, 'in_progress')}
                    >
                      Start
                    </button>
                    <button
                      className="button button--delete badge"
                      onClick={() => handleUpdateOrderStatus(order.repair_order_id, 'cancelled')}
                    >
                      Cancel
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Home;
