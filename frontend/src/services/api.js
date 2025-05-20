import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const getCustomers = async () => {
  try {
    const response = await axios.get(API_URL + '/customers/list');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching customers:', error);
    return [];
  }
};

export const getCustumer = async (id) => {
  try {
    const response = await axios.get(API_URL + '/customers/detail/' + id);
    return response.data;
  } catch (error) {
    console.error('Error fetching customer:', error);
    return null;
  }
}

export const deleteCustomer = async (id) => {
  try {
    const response = await axios.delete(API_URL + '/customers/delete/' + id);
    return response.status === 204
  } catch (error) {
    console.error('Error deleting customer:', error);
    return false;
  }
};

export const createCustomer = async (customer) => {
  try {
    const response = await axios.post(API_URL + '/customers/create', customer);
    return response.data;
  } catch (error) {
    console.error('Error creating customer:', error);
    return null
  }
};

export const editCustomer = async (customer) => {
  try {
    const response = await axios.put(API_URL + '/customers/update/' + customer.id, { "name": customer.name, "email": customer.email, "phone": customer.phone, "address": customer.address });
    return response.data;
  } catch (error) {
    console.error('Error editing customer:', error);
    return null;
  }
};