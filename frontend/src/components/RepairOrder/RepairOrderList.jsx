import { useEffect, useState } from "react";
import Header from "../Header";
import { getOrders } from "../../services/repairOrderApi";
import { useNavigate } from "react-router-dom";

const RepairOrderList = () => {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getOrders();
      setOrders(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div>
      <Header title="Repair Orders" />
      <div className="repair-order-list-container">
        <button
          className="button button--success"
          disabled={loading}
          onClick={() => navigate("/repair-orders/create")}
        >
          Add Order
        </button>
        {loading ? (
          <div className="repair-order-row">
            <p>Loading orders...</p>
          </div>
        ) : (
          <table className="short-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Status</th>
                <th>Date In</th>
                <th>Date Expected Out</th>
                <th>Vehicle</th>
                <th>Customer</th>
                <th>Labor Cost</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr
                  key={order.id}
                  className={`repair-order-row${order.status === 'completed' || order.status === 'cancelled' ? ' is-completed' : ''}`}
                >
                  <td>{order.id}</td>
                  <td>{order.status}</td>
                  <td>{new Date(order.date_in).toLocaleDateString()}</td>
                  <td>{order.date_expected_out ? new Date(order.date_expected_out).toLocaleDateString() : 'Not set'}</td>
                  <td>{order.vehicle?.license_plate || 'N/A'}</td>
                  <td>{order.customer?.name || 'N/A'}</td>
                  <td>${order.labor_cost.toFixed(2)}</td>
                  <td>
                    <button
                      className="button button--info badge"
                      onClick={() => navigate(`/repair-orders/detail/${order.id}`)}
                    >
                      View
                    </button>
                    {order.status !== 'completed' && order.status !== 'cancelled' && (
                      <button
                        className="button button--edit badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/repair-orders/edit/${order.id}`);
                        }}
                      >
                        Edit
                      </button>
                    )}
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

export default RepairOrderList;
