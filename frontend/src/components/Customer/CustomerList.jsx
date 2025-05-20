import { useEffect, useState } from "react";
import Header from "../Header";
import { deleteCustomer, getCustomers } from "../../services/customerApi";
import { useNavigate } from "react-router-dom";

const CustomerList = () => {

  const navigate = useNavigate()

  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getCustomers();
      setCustomers(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  const handleDelete = async (customer) => {
    if (window.confirm(`Are you sure you want to delete the customer ${customer.name}?`)) {
      const id = customer.id
      setDeleting(id)
      const result = await deleteCustomer(id)
      if (result) {
        const data = await getCustomers();
        setCustomers(data);
      } else {
        alert(`Could not delete the customer ${customer.name}`);
      }
      setDeleting(null)
    }
  };

  return (
    <div>
      <Header title="Customers" />
      <div className="customer-list-container">
        <button className="button button--success" disabled={loading} onClick={() => navigate("/customers/new")}>{"Add Customer"}</button>
        {loading ?
          <p>Loading customers...</p>
          :
          (
            <table className="customer-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer) => (
                  <tr
                    key={customer.id}
                    className="customer-row"
                  >
                    <td>{customer.name}</td>
                    <td>{customer.email}</td>
                    <td>{customer.phone}</td>
                    <td>
                      <button
                        className="button button--info badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/customers/detail/${customer.id}`)
                        }}
                      >
                        View
                      </button>
                      <button
                        className="button button--edit badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/customers/edit/${customer.id}`)
                        }}
                      >
                        Edit
                      </button>
                      <button
                        className="button button--delete badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(customer);
                        }}
                        disabled={deleting === customer.id}
                      >
                        {deleting === customer.id ? "Deleting" : "Delete"}
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

export default CustomerList;
