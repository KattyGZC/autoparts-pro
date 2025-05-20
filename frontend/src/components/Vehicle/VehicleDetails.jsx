import { useEffect, useState } from 'react';
import Header from '../Header';
import { getVehicle, deleteVehicle } from '../../services/vehicleApi';
import { useNavigate, useParams } from 'react-router-dom';

const VehicleDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

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
                  <p><strong>Customer:</strong> <span className={vehicle.customer.is_active ? '' : 'is-not-active'}>{vehicle.customer.name}</span></p>
                </div>
                <button
                  className="button button--edit"
                  onClick={() => navigate(`/vehicles/edit/${vehicle.id}`)}
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
              </div>
            )}
      </div>
    </div>
  );
};

export default VehicleDetails;
