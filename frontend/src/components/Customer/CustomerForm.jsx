import { useEffect, useState } from 'react';
import Header from '../Header';
import { createCustomer, editCustomer, getCustumer } from '../../services/customerApi';
import { useNavigate, useParams } from 'react-router-dom';

const CustomerForm = () => {
  const params = useParams();
  const [customerParam, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomer = async () => {
      if (params.id) {
        setLoading(true);
        const customer = await getCustumer(params.id);
        setCustomer(customer)
        setCustomerData(customer)
        setLoading(false);
      }
    };
    fetchCustomer();
  }, [params.id]);

  const [customerData, setCustomerData] = useState({
    name: customerParam?.name || '',
    email: customerParam?.email || '',
    phone: customerParam?.phone || '',
    address: customerParam?.address || '',
  });

  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomerData({ ...customerData, [name]: value })
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (customerParam) {
      try {
        const customerEdited = await editCustomer(customerData);
        if (customerEdited) {
          navigate(`/customers/detail/${customerEdited.id}`, { replace: true });
        } else {
          alert('Failed to edit customer. Please try again.');
        }
      } catch (error) {
        console.error('Error editing customer:', error);
        alert('Failed to edit customer. Please try again.');
      }
    } else {
      const newCostumer = await createCustomer(customerData)
      if (newCostumer) {
        navigate('/customers')
      } else {
        alert('Failed to create customer. Please try again.')
      }
    }
  };

  return (
    <div className="customer-form-container">
      <Header title={customerParam ? "Edit Customer" : "Create New Customer"} />
      <div className="customer-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input id="name" type="text" name="name" value={customerData?.name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input id="email" type="email" name="email" value={customerData?.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="phone">Phone:</label>
            <input id="phone" type="tel" name="phone" value={customerData?.phone} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="address">Address:</label>
            <input id="address" type="text" name="address" value={customerData?.address} onChange={handleChange} required />
          </div>
          <button type="submit" className="submit-button">{customerParam ? "Edit Customer" : "Create Customer"}</button>
        </form>
      </div>
    </div>
  );
};

export default CustomerForm;