import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const getVehicles = async () => {
  try {
    const response = await axios.get(API_URL + '/vehicles/list');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching vehicles:', error);
    return [];
  }
};

export const getVehicle = async (id) => {
  try {
    const response = await axios.get(API_URL + '/vehicles/detail/' + id);
    return response.data;
  } catch (error) {
    console.error('Error fetching vehicle:', error);
    return null;
  }
};

export const deleteVehicle = async (id) => {
  try {
    const response = await axios.delete(API_URL + '/vehicles/delete/' + id);
    return response.status === 204;
  } catch (error) {
    console.error('Error deleting vehicle:', error);
    return false;
  }
};

export const createVehicle = async (vehicle) => {
  try {
    const response = await axios.post(API_URL + '/vehicles/create', vehicle);
    return response.data;
  } catch (error) {
    console.error('Error creating vehicle:', error);
    return null;
  }
};

export const editVehicle = async (vehicle) => {
  try {
    const response = await axios.put(API_URL + '/vehicles/update/' + vehicle.id, {
      "license_plate": vehicle.license_plate,
      "model": vehicle.model,
      "brand": vehicle.brand,
      "year": vehicle.year,
      "color": vehicle.color,
      "customer_id": vehicle.customer_id
    });
    return response.data;
  } catch (error) {
    console.error('Error editing vehicle:', error);
    return null;
  }
};

export const getVehiclesByCustomer = async (customerId) => {
  try {
    const response = await axios.get(`${API_URL}/vehicles/customer/${customerId}`);
    return response.data || [];
  } catch (error) {
    console.error('Error fetching vehicles for customer:', error);
    return [];
  }
};
