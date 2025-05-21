import { useEffect, useState } from 'react';
import Header from '../Header';
import { createOrder } from '../../services/repairOrderApi';
import { getVehiclesByCustomer } from '../../services/vehicleApi';
import { getCustomers } from '../../services/customerApi';
import { useNavigate, useLocation } from 'react-router-dom';

const RepairOrderCreate = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [vehicles, setVehicles] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loadingVehicles, setLoadingVehicles] = useState(true);
  const [loadingCustomers, setLoadingCustomers] = useState(true);
  const vehicleId = new URLSearchParams(location.search).get('vehicle_id');
  const customerId = new URLSearchParams(location.search).get('customer_id');
  const [orderData, setOrderData] = useState({
    customer_id: customerId || '',
    vehicle_id: vehicleId || '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setOrderData({ ...orderData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const orderCreated = await createOrder(orderData);
      if (orderCreated) {
        navigate(`/repair-orders/detail/${orderCreated.id}`, { replace: true });
      } else {
        alert('Failed to create repair order. Please try again.');
      }
    } catch (error) {
      console.error('Error creating repair order:', error);
      alert('Failed to create repair order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchCustomers = async () => {
      setLoadingCustomers(true);
      try {
        const customers = await getCustomers();
        setCustomers(customers);
      } catch (error) {
        console.error('Error fetching customers:', error);
      } finally {
        setLoadingCustomers(false);
      }
    };
    fetchCustomers();
  }, []);

  useEffect(() => {
    const fetchVehicles = async () => {
      if (!orderData.customer_id) return;
      setLoadingVehicles(true);
      try {
        const vehicles = await getVehiclesByCustomer(orderData.customer_id);
        setVehicles(vehicles);
      } catch (error) {
        console.error('Error fetching vehicles:', error);
      } finally {
        setLoadingVehicles(false);
      }
    };
    fetchVehicles();
  }, [orderData.customer_id]);

  return (
    <div className="order-form-container">
      <Header title="Create New Repair Order" />
      <div className="order-form">
        <form onSubmit={handleSubmit}>

          <div className="form-group">
            <label htmlFor="customer_id">Customer:</label>
            <select
              id="customer_id"
              name="customer_id"
              value={orderData.customer_id}
              onChange={handleChange}
              required
              disabled={loading || loadingCustomers}
              className="select-control"
            >
              <option value="">Select a customer</option>
              {customers.map(customer => (
                <option key={customer.id} value={customer.id}>
                  {customer.name} ({customer.email})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="vehicle_id">Vehicle:</label>
            <select
              id="vehicle_id"
              name="vehicle_id"
              value={orderData.vehicle_id}
              onChange={handleChange}
              required
              disabled={loading || loadingVehicles}
              className="select-control"
            >
              <option value="">Select a vehicle</option>
              {vehicles.map(vehicle => (
                <option key={vehicle.id} value={vehicle.id}>
                  {vehicle.license_plate} - {vehicle.brand} {vehicle.model} ({vehicle.year})
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="button button--success" disabled={loading}>
            Create Repair Order
          </button>
        </form>
      </div>
    </div>
  );
};

export default RepairOrderCreate;
