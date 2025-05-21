import { useEffect, useState } from 'react';
import Header from '../Header';
import { getVehicle, deleteVehicle } from '../../services/vehicleApi';
import { getOrdersByVehicle } from '../../services/repairOrderApi';
import { useNavigate, useParams } from 'react-router-dom';

const VehicleDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);
  const [loadingOrders, setLoadingOrders] = useState(true);
  const [orders, setOrders] = useState([]);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete vehicle ${vehicle.license_plate}?`)) {
      const id = vehicle.id;
      setDeleting(id);
      const result = await deleteVehicle(id);
      if (result) {
        navigate('/vehicles', { replace: true });
      } else {
        alert(`Could not delete vehicle ${vehicle.license_plate}`);
      }
      setDeleting(null);
    }
  };

  useEffect(() => {
    const fetchVehicle = async () => {
      setLoading(true);
      const data = await getVehicle(id);
      setVehicle(data);
      setLoading(false);
    };

    fetchVehicle();
  }, [id]);

  useEffect(() => {
    const fetchOrders = async () => {
      if (vehicle?.id) {
        setLoadingOrders(true);
        const orders = await getOrdersByVehicle(vehicle.id);
        setOrders(orders);
        setLoadingOrders(false);
      }
    };

    fetchOrders();
  }, [vehicle?.id]);

  return (
    <div>
      <Header title="Vehicle Details" />
      <div className="vehicle-details-container">
        {loading ? <p>Loading...</p> :
          !vehicle ? <p>No vehicle found.</p> :
            (
              <div>
                <div className="vehicle-details">
                  <p><strong>License Plate:</strong> {vehicle.license_plate}</p>
                  <p><strong>Model:</strong> {vehicle.model}</p>
                  <p><strong>Brand:</strong> {vehicle.brand}</p>
                  <p><strong>Year:</strong> {vehicle.year}</p>
                  <p><strong>Color:</strong> {vehicle.color}</p>
                  <p><strong>Customer:</strong> <a href={`/customers/detail/${vehicle.customer.id}`} className={vehicle.customer.is_active ? '' : 'is-not-active'}>{vehicle.customer.name}</a>
                    {!vehicle.customer.is_active && (
                      <button
                        className="button button--info badge"
                        disabled={!vehicle.customer.is_active}
                        style={{ marginLeft: "10px", cursor: "default" }}
                      >
                        Inactive
                      </button>
                    )}
                  </p>
                  <p><strong>Vehicle Active:</strong> {vehicle.is_active ? 'Yes' : 'No'}</p>
                </div>
                <button
                  className="button button--success"
                  onClick={() => navigate(`/repair-orders/create?vehicle_id=${vehicle.id}&customer_id=${vehicle.customer.id}`)}
                >
                  Create Repair Order
                </button>
                <button
                  className="button button--edit"
                  onClick={() => navigate(`/vehicles/edit/${vehicle.id}`)}
                  style={{ marginLeft: "10px" }}
                >
                  Edit
                </button>
                <button
                  className="button button--delete"
                  onClick={handleDelete}
                  disabled={deleting}
                  style={{ marginLeft: "10px" }}
                >
                  {deleting ? "Deleting..." : "Delete"}
                </button>
                <h4>REPAIR ORDERS</h4>
                <div className="orders-list">
                  {loadingOrders ? <p>Loading orders...</p> :
                    orders.length === 0 ? (
                      <p>No repair orders for this vehicle.</p>
                    ) : (
                      <table className="short-table">
                        <thead>
                          <tr>
                            <th>Order ID</th>
                            <th>Status</th>
                            <th>Date in</th>
                            <th>Date out</th>
                            <th></th>
                          </tr>
                        </thead>
                        <tbody>
                          {orders.map((order) => (
                            <tr key={order.id}>
                              <td>{order.id}</td>
                              <td>{order.status}</td>
                              <td>{new Date(order.date_in).toLocaleDateString()}</td>
                              <td>{new Date(order.date_out).toLocaleDateString()}</td>
                              <td>
                                <button
                                  className="button button--info badge"
                                  onClick={() => navigate(`/repair-orders/detail/${order.id}`)}
                                >
                                  View
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                </div>
              </div>
            )}
      </div>
    </div>
  );
};

export default VehicleDetails;
