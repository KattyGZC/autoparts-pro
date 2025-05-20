import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const getOrdersByVehicle = async (vehicleId) => {
  try {
    const response = await axios.get(API_URL + '/repair_orders/vehicle/' + vehicleId);
    return response.data || [];
  } catch (error) {
    console.error('Error fetching orders:', error);
    return [];
  }
};
