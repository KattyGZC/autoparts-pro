import { customersDB } from "./fakeData";

const DELAY = 500

export const getCustomers = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(customersDB);
    }, DELAY);
  });
};

export const deleteCustomer = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, DELAY);
  });
};