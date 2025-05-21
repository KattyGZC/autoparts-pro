import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const getOptimizedOrders = async () => {
  try {
    const response = await axios.get(API_URL + '/repair_order_optimization/list');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching optimized orders:', error);
    return [];
  }
};

export const getOrders = async () => {
  try {
    const response = await axios.get(API_URL + '/repair_orders/list');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching orders:', error);
    return [];
  }
};

export const getOrder = async (id) => {
  try {
    const response = await axios.get(API_URL + '/repair_orders/detail/' + id);
    return response.data;
  } catch (error) {
    console.error('Error fetching order:', error);
    return null;
  }
};

export const createOrder = async (order) => {
  try {
    const response = await axios.post(API_URL + '/repair_orders/create', order);
    return response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    return null;
  }
};

export const editOrder = async (order) => {
  try {
    const response = await axios.put(API_URL + '/repair_orders/update/' + order.id, order);
    return response.data;
  } catch (error) {
    console.error('Error editing order:', error);
    return null;
  }
};

export const getOrdersByVehicle = async (vehicleId) => {
  try {
    const response = await axios.get(API_URL + '/repair_orders/vehicle/' + vehicleId);
    return response.data || [];
  } catch (error) {
    console.error('Error fetching orders:', error);
    return [];
  }
};

// Status: 'cancelled' | 'completed' | 'in_progress' | 'pending'
export const updateOrderStatus = async (orderId, status) => {
  try {
    const response = await axios.patch(API_URL + '/repair_orders/update-status/' + orderId, { status });
    return response.data;
  } catch (error) {
    console.error('Error updating order status:', error);
    return null;
  }
};
