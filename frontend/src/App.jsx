import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import CustomerList from "./components/Customer/CustomerList";
import VehicleList from "./components/Vehicle/VehicleList";
import InventoryList from "./components/InventoryParts/InventoryList";
import RepairOrderList from "./components/RepairOrder/RepairOrderList";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/customers" element={<CustomerList />} />
        <Route path="/vehicles" element={<VehicleList />} />
        <Route path="/inventory" element={<InventoryList />} />
        <Route path="/repair-orders" element={<RepairOrderList />} />
        <Route path="*" element={<h2 style={{ color: "red" }}>404 - Page Not Found</h2>} />
      </Routes>
    </Router>
  );
};

export default App;
