import { useEffect, useState } from "react";
import Header from "../Header";
import { useNavigate, useParams } from "react-router-dom";
import { getCustumer } from "../../services/api";

const CustomerDetails = () => {
  const navigate = useNavigate();
  const params = useParams();
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

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
                  className="edit-customer-button"
                  onClick={() => navigate(`/customers/edit/${customer.id}`)}
                >
                  Edit
                </button>
              </div>
            )}

      </div>
    </div>
  );
};

export default CustomerDetails;