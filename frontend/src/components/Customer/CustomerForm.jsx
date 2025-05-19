import { useState } from 'react';
import Header from '../Header';
import { createCustomer } from '../../services/api';
import { useNavigate } from 'react-router-dom';

const CustomerForm = () => {
  const [customerData, setCustomerData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
  });

  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomerData({ ...customerData, [name]: value })
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newCostumer = await createCustomer(customerData)
    if (newCostumer) {
      navigate('/customers')
    } else {
      alert('Failed to create customer. Please try again.')
    }
  };

  return (
    <div className="customer-form-container">
      <Header title="Create New Customer" />
      <div className="customer-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input id="name" type="text" name="name" value={customerData.name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input id="email" type="email" name="email" value={customerData.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="phone">Phone:</label>
            <input id="phone" type="tel" name="phone" value={customerData.phone} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="address">Address:</label>
            <input id="address" type="text" name="address" value={customerData.address} onChange={handleChange} required />
          </div>
          <button type="submit" className="submit-button">Create Customer</button>
        </form>
      </div>
    </div>
  );
};

export default CustomerForm;