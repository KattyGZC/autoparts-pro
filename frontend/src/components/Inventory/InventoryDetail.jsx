import { useEffect, useState } from "react";
import Header from "../Header";
import { useNavigate, useParams } from "react-router-dom";
import { deleteInventoryPart, getInventoryPart } from "../../services/inventoryApi";

const InventoryDetail = () => {
  const navigate = useNavigate();
  const params = useParams();
  const [part, setPart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete the inventory part ${part.name}?`)) {
      const id = part.id;
      setDeleting(true);
      const result = await deleteInventoryPart(id);
      if (result) {
        navigate(`/inventory`, { replace: true });
      } else {
        alert(`Could not delete the inventory part ${part.name}`);
      }
      setDeleting(false);
    }
  };

  useEffect(() => {
    const fetchPart = async () => {
      setLoading(true);
      const part = await getInventoryPart(params.id);
      setPart(part);
      setLoading(false);
    };
    fetchPart();
  }, [params.id]);

  return (
    <div>
      <Header title="Inventory Part Details" />
      <div className="inventory-details-container">
        {loading ? <p>Loading...</p> :
          !part ? <p>No inventory part found.</p> :
            (
              <div>
                <div className="inventory-details">
                  <p><strong>Name:</strong> {part.name}</p>
                  <p><strong>Description:</strong> {part.description}</p>
                  <p><strong>Stock Quantity:</strong> {part.stock_quantity}</p>
                  <p><strong>Cost:</strong> ${part.cost.toFixed(2)}</p>
                </div>
                <button
                  className="button button--edit"
                  onClick={() => navigate(`/inventory/edit/${part.id}`)}
                  style={{ marginLeft: "10px" }}
                >
                  Edit Part
                </button>
                <button
                  className="button button--delete"
                  onClick={handleDelete}
                  disabled={deleting}
                  style={{ marginLeft: "10px" }}
                >
                  {deleting ? "Deleting Part..." : "Delete Part"}
                </button>
              </div>
            )}
      </div>
    </div>
  );
};

export default InventoryDetail;