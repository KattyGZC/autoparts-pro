import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const getInventory = async () => {
  try {
    const response = await axios.get(API_URL + '/inventory_parts/list');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching inventory:', error);
    return [];
  }
};

export const getInventoryPart = async (id) => {
  try {
    const response = await axios.get(API_URL + '/inventory_parts/detail/' + id);
    return response.data;
  } catch (error) {
    console.error('Error fetching inventory part:', error);
    return null;
  }
}

export const deleteInventoryPart = async (id) => {
  try {
    const response = await axios.patch(API_URL + '/inventory_parts/disable/' + id);
    return response.status === 204;
  } catch (error) {
    console.error('Error deleting inventory part:', error);
    return false;
  }
};

export const createInventoryPart = async (inventoryPart) => {
  try {
    const response = await axios.post(API_URL + '/inventory_parts/create', inventoryPart);
    return response.data;
  } catch (error) {
    console.error('Error creating inventory part:', error);
    return null;
  }
};

export const editInventoryPart = async (inventoryPart) => {
  try {
    const response = await axios.put(API_URL + '/inventory_parts/update/' + inventoryPart.id, inventoryPart);
    return response.data;
  } catch (error) {
    console.error('Error editing inventory part:', error);
    return null;
  }
};
