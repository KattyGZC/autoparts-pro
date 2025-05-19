import { useEffect, useState } from "react";
import Header from "../Header";
import { deleteCustomer, getCustomers } from "../../services/api";

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
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
        setCustomers(customers.filter((customer) => customer.id !== id));
      } else {
        alert(`Could not delete the customer ${customer.name}`);
      }
      setDeleting(null)
    }
  };

  const handleDetails = (customer) => {
    alert(`Details for ${customer.name}`);
  };

  return (
    <div>
      <Header title="Customers" />
      <div className="customer-list-container">
        <button className="new-customer-button" disabled={creating || loading}>{creating ? "Adding..." : "Add Customer"}</button>
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
                  <th>Address</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {customers.map((customer) => (
                  <tr
                    key={customer.id}
                    className="customer-row"
                    onClick={() => handleDetails(customer)}
                    style={{ cursor: "pointer" }}
                  >
                    <td>{customer.name}</td>
                    <td>{customer.email}</td>
                    <td>{customer.phone}</td>
                    <td>{customer.address}</td>
                    <td>
                      <button
                        className="delete-button"
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
