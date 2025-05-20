import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import CustomerList from "./components/Customer/CustomerList";
import VehicleList from "./components/Vehicle/VehicleList";
import VehicleForm from "./components/Vehicle/VehicleForm";
import VehicleDetails from "./components/Vehicle/VehicleDetails";
import InventoryList from "./components/Inventory/InventoryList";
import RepairOrderList from "./components/RepairOrder/RepairOrderList";
import CustomerForm from "./components/Customer/CustomerForm";
import CustomerDetails from "./components/Customer/CustomerDetails";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/customers" element={<CustomerList />} />
        <Route path="/customers/new" element={<CustomerForm />} />
        <Route path="/customers/detail/:id" element={<CustomerDetails />} />
        <Route path="/customers/edit/:id" element={<CustomerForm />} />
        <Route path="/vehicles" element={<VehicleList />} />
        <Route path="/vehicles/new" element={<VehicleForm />} />
        <Route path="/vehicles/detail/:id" element={<VehicleDetails />} />
        <Route path="/vehicles/edit/:id" element={<VehicleForm />} />
        <Route path="/inventory" element={<InventoryList />} />
        <Route path="/repair-orders" element={<RepairOrderList />} />
        <Route path="*" element={<h2 style={{ color: "red" }}>404 - Page Not Found</h2>} />
      </Routes>
    </Router>
  );
};

export default App;
