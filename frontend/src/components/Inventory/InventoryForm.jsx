import { useEffect, useState } from 'react';
import Header from '../Header';
import { createInventoryPart, editInventoryPart, getInventoryPart } from '../../services/inventoryApi';
import { useNavigate, useParams } from 'react-router-dom';

const InventoryForm = () => {
  const params = useParams();
  const [partParam, setPart] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchPart = async () => {
      if (params.id) {
        setLoading(true);
        const part = await getInventoryPart(params.id);
        setPart(part);
        setPartData(part);
        setLoading(false);
      }
    };
    fetchPart();
  }, [params.id]);

  const [partData, setPartData] = useState({
    name: partParam?.name || '',
    description: partParam?.description || '',
    stock_quantity: partParam?.stock_quantity || 0,
    cost: partParam?.cost || 0,
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPartData({ ...partData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (partParam) {
        const partEdited = await editInventoryPart(partData);
        if (partEdited) {
          navigate(`/inventory/detail/${partEdited.id}`, { replace: true });
        } else {
          alert('Failed to edit inventory part. Please try again.');
        }
      } else {
        const newPart = await createInventoryPart(partData);
        if (newPart) {
          navigate('/inventory', { replace: true });
        } else {
          alert('Failed to create inventory part. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error saving inventory part:', error);
      alert('Failed to save inventory part. Please try again.');
    }
  };

  return (
    <div className="inventory-form-container">
      <Header title={partParam ? "Edit Inventory Part" : "Create New Inventory Part"} />
      <div className="inventory-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input 
              id="name" 
              disabled={loading} 
              type="text" 
              name="name" 
              value={partData?.name} 
              onChange={handleChange} 
              required 
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description:</label>
            <textarea 
              id="description" 
              disabled={loading} 
              name="description" 
              value={partData?.description} 
              onChange={handleChange} 
              rows="3"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="stock_quantity">Stock Quantity:</label>
            <input 
              id="stock_quantity" 
              disabled={loading} 
              type="number" 
              name="stock_quantity" 
              value={partData?.stock_quantity} 
              onChange={handleChange} 
              min="0"
              required 
            />
          </div>
          <div className="form-group">
            <label htmlFor="cost">Cost:</label>
            <input 
              id="cost" 
              disabled={loading} 
              type="number" 
              name="cost" 
              value={partData?.cost} 
              onChange={handleChange} 
              min="0"
              step="0.01"
              required 
            />
          </div>
          <button 
            disabled={loading} 
            type="submit" 
            className="button button--success"
          >
            {partParam ? "Edit Inventory Part" : "Create Inventory Part"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default InventoryForm;