import { useEffect, useState } from "react";
import Header from "../Header";
import { deleteInventoryPart, getInventory } from "../../services/inventoryApi";
import { useNavigate } from "react-router-dom";

const InventoryList = () => {
  const navigate = useNavigate()

  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getInventory();
      setInventory(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  const handleDelete = async (part) => {
    if (window.confirm(`Are you sure you want to delete the inventory part ${part.name}?`)) {
      const id = part.id;
      setDeleting(id);
      const result = await deleteInventoryPart(id);
      if (result) {
        const data = await getInventory();
        setInventory(data);
      } else {
        alert(`Could not delete the inventory part ${part.name}`);
      }
      setDeleting(null);
    }
  };

  return (
    <div>
      <Header title="Inventory" />
      <div className="inventory-list-container">
        <button className="button button--success" disabled={loading} onClick={() => navigate("/inventory/new")}>Add Part</button>
        {loading ?
          <p>Loading inventory...</p>
          :
          (
            <table className="inventory-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Cost</th>
                  <th>Stock Quantity</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {inventory.map((part) => (
                  <tr
                    key={part.id}
                    className="inventory-row"
                  >
                    <td>{part.name}</td>
                    <td>${part.cost.toFixed(2)}</td>
                    <td>{part.stock_quantity}</td>
                    <td>
                      <button
                        className="button button--info badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/inventory/detail/${part.id}`)
                        }}
                      >
                        View
                      </button>
                      <button
                        className="button button--edit badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/inventory/edit/${part.id}`)
                        }}
                      >
                        Edit
                      </button>
                      <button
                        className="button button--delete badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(part);
                        }}
                        disabled={deleting === part.id}
                      >
                        {deleting === part.id ? "Deleting..." : "Delete"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
      </div>
    </div>
  );
};

export default InventoryList;
