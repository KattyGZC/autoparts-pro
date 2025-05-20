import { useEffect, useState } from "react";
import Header from "../Header";
import { deleteVehicle, getVehicles } from "../../services/vehicleApi";
import { useNavigate } from "react-router-dom";

const VehicleList = () => {
  const navigate = useNavigate();
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getVehicles();
      setVehicles(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  const handleDelete = async (vehicle) => {
    if (window.confirm(`Are you sure you want to delete vehicle ${vehicle.license_plate}?`)) {
      const id = vehicle.id;
      setDeleting(id);
      const result = await deleteVehicle(id);
      if (result) {
        const data = await getVehicles();
        setVehicles(data);
      } else {
        alert(`Could not delete vehicle ${vehicle.license_plate}`);
      }
      setDeleting(null);
    }
  };

  return (
    <div>
      <Header title="Vehicles" />
      <div className="vehicle-list-container">
        <button className="button button--success" disabled={loading} onClick={() => navigate("/vehicles/new")}>{"Add Vehicle"}</button>
        {loading ? (
          <div className="vehicle-row">
            <p>Loading vehicles...</p>
          </div>
        ) : (
          <table className="vehicle-table">
            <thead>
              <tr>
                <th>Brand</th>
                <th>Year</th>
                <th>Color</th>
                <th>License Plate</th>
                <th>Customer</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {vehicles.map((vehicle) => (
                <tr
                  key={vehicle.id}
                  className={`vehicle-row${vehicle.is_active ? '' : ' is-not-active'}`}
                >
                  <td>{vehicle.brand}</td>
                  <td>{vehicle.year}</td>
                  <td>{vehicle.color}</td>
                  <td>{vehicle.license_plate}</td>
                  <td className={vehicle.customer.is_active ? '' : 'is-not-active'}>{vehicle.customer.name}</td>
                  <td>
                    <button
                      className="button button--info badge"
                      onClick={() => navigate(`/vehicles/detail/${vehicle.id}`)}
                    >
                      View
                    </button>
                    <button
                      className="button button--edit badge"
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/vehicles/edit/${vehicle.id}`);
                      }}
                    >
                      Edit
                    </button>
                    <button
                      className="button button--delete badge"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(vehicle);
                      }}
                      disabled={deleting === vehicle.id}
                    >
                      {deleting === vehicle.id ? "Deleting" : "Delete"}
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

export default VehicleList;
