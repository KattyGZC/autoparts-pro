import { useEffect, useState } from "react";
import Header from "../Header";
import { useNavigate, useParams } from "react-router-dom";
import { deleteCustomer, getCustumer } from "../../services/customerApi";

const CustomerDetails = () => {
  const navigate = useNavigate();
  const params = useParams();
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete the customer ${customer.name}?`)) {
      const id = customer.id
      setDeleting(id)
      const result = await deleteCustomer(id)
      if (result) {
        navigate(`/customers`, { replace: true });
      } else {
        alert(`Could not delete the customer ${customer.name}`);
      }
      setDeleting(null)
    }
  };

  useEffect(() => {
    const fetchCustomer = async () => {
      setLoading(true);
      const customer = await getCustumer(params.id);
      setCustomer(customer)
      setLoading(false);
    };
    fetchCustomer();
  }, [params.id]);

  return (
    <div>
      <Header title="Customer Details" />
      <div className="customer-details-container">
        {loading ? <p>Loading...</p> :
          !customer ? <p>No customer found.</p> :
            (
              <div>
                <div className="customer-details">
                  <p><strong>Name:</strong> {customer.name}</p>
                  <p><strong>Email:</strong> {customer.email}</p>
                  <p><strong>Phone:</strong> {customer.phone}</p>
                  <p><strong>Address:</strong> {customer.address}</p>
                </div>
                <button
                  className="button button--success"
                  onClick={() => navigate(`/vehicles/new?customerId=${customer.id}`)}
                >
                  Add Vehicle
                </button>
                <button
                  className="button button--edit"
                  onClick={() => navigate(`/customers/edit/${customer.id}`)}
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
              </div>
            )}

      </div>
    </div>
  );
};

export default CustomerDetails;