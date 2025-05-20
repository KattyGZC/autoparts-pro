import { useEffect, useState } from 'react';
import Header from '../Header';
import { createVehicle, editVehicle, getVehicle } from '../../services/vehicleApi';
import { getCustomers } from '../../services/customerApi';
import { useNavigate, useParams } from 'react-router-dom';

const VehicleForm = () => {
  const navigate = useNavigate();
  const params = useParams();
  const [vehicleParam, setVehicleParam] = useState(null);
  const [loading, setLoading] = useState(false);
  const [customers, setCustomers] = useState([]);
  const [loadingCustomers, setLoadingCustomers] = useState(true);
  const [vehicleData, setVehicleData] = useState({
    license_plate: vehicleParam?.license_plate || '',
    model: vehicleParam?.model || '',
    brand: vehicleParam?.brand || '',
    year: vehicleParam?.year || '',
    color: vehicleParam?.color || '',
    customer_id: vehicleParam?.customer_id || params.customerId || '',
  });

  console.log(params);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setVehicleData({ ...vehicleData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (vehicleParam) {
      try {
        const vehicleEdited = await editVehicle(vehicleData);
        if (vehicleEdited) {
          navigate(`/vehicles/detail/${vehicleEdited.id}`, { replace: true });
        } else {
          alert('Failed to edit vehicle. Please try again.');
        }
      } catch (error) {
        console.error('Error editing vehicle:', error);
        alert('Failed to edit vehicle. Please try again.');
      }
    } else {
      try {
        const vehicleCreated = await createVehicle(vehicleData);
        if (vehicleCreated) {
          navigate(`/vehicles/detail/${vehicleCreated.id}`);
        } else {
          alert('Failed to create vehicle. Please try again.');
        }
      } catch (error) {
        console.error('Error creating vehicle:', error);
        alert('Failed to create vehicle. Please try again.');
      }
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
    const fetchVehicle = async () => {
      if (params.id) {
        setLoading(true);
        const vehicle = await getVehicle(params.id);
        setVehicleParam(vehicle);
        setVehicleData(vehicle);
        setLoading(false);
      }
    };
    fetchVehicle();
  }, [params.id]);

  return (
    <div className="vehicle-form-container">
      <Header title={vehicleParam ? 'Edit Vehicle' : 'Create New Vehicle'} />
      <div className="vehicle-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="license_plate">License Plate:</label>
            <input
              id="license_plate"
              type="text"
              name="license_plate"
              value={vehicleData.license_plate}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="model">Model:</label>
            <input
              id="model"
              type="text"
              name="model"
              value={vehicleData.model}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="brand">Brand:</label>
            <input
              id="brand"
              type="text"
              name="brand"
              value={vehicleData.brand}
              onChange={handleChange}
              required
              disabled={loading}
              className="form-control"
            />
          </div>
          <div className="form-group">
            <label htmlFor="year">Year:</label>
            <input
              id="year"
              type="number"
              name="year"
              value={vehicleData.year}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="color">Color:</label>
            <input
              id="color"
              type="text"
              name="color"
              value={vehicleData.color}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="customer_id">Customer:</label>
            <select
              id="customer_id"
              name="customer_id"
              value={vehicleData.customer_id}
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
          <button type="submit" className="button button--success" disabled={loading}>
            {vehicleParam ? 'Edit Vehicle' : 'Create Vehicle'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default VehicleForm;