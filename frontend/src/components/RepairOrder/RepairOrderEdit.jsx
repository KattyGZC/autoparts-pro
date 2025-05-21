import { useEffect, useState } from 'react';
import Header from '../Header';
import { editOrder, getOrder } from '../../services/repairOrderApi';
import { getInventoryPartsByOrder, getInventory } from '../../services/inventoryApi';
import { useNavigate, useParams } from 'react-router-dom';

const RepairOrderEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [order, setOrder] = useState(null);
  const [parts, setParts] = useState([]);
  const [loadingInventory, setLoadingInventory] = useState(false);
  const [inventory, setInventory] = useState([]);
  const [newPartId, setNewPartId] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoadingInventory(true);
      const data = await getInventory();
      setInventory(data);
      setLoadingInventory(false);
    };

    fetchData();
  }, []);

  const handleQuantityChange = (partId, quantity) => {
    setParts(prevParts => prevParts.map(part =>
      part.id === partId
        ? { ...part, quantity_used: quantity }
        : part
    ));
  };

  const handleDeletePart = (partId) => {
    setParts(prevParts => prevParts.filter(part => part.id !== partId));
  };

  const handleAddPart = () => {
    const newPart = inventory.find(item => item.id === newPartId);
    if (newPart) {
      setParts(prevParts => [...prevParts, {
        ...newPart,
        quantity_used: 1,
        final_price: newPart.final_price
      }]);
      setNewPartId('');
    }
  };

  useEffect(() => {
    const fetchOrder = async () => {
      setLoading(true);
      try {
        const data = await getOrder(id);
        const parts = await getInventoryPartsByOrder(id);
        setOrder(data);
        setParts(parts);
      } catch (error) {
        console.error('Error fetching order:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setOrder({ ...order, [name]: value });
  };

  const handleDateChange = (e) => {
    const { name, value } = e.target;
    setOrder({ ...order, [name]: value ? new Date(value).toISOString() : null });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const orderFormated = {
        id: order.id,
        status: order.status,
        labor_cost: order.labor_cost,
        date_expected_out: order.date_expected_out,
        date_out: order.status === 'completed' || order.status === 'cancelled' ? order.date_out : null,
        total_cost_repair: order.total_cost_repair,
        parts: parts.map(part => ({
          part_id: part.id,
          quantity: part.quantity_used,
        }))
      }
      setLoading(true);
      const orderUpdated = await editOrder(orderFormated);
      if (orderUpdated) {
        navigate(`/repair-orders/detail/${orderFormated.id}`, { replace: true });
      } else {
        alert('Failed to update repair order. Please try again.');
      }
    } catch (error) {
      console.error('Error updating repair order:', error);
      alert('Failed to update repair order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="order-form-container">
      <Header title="Edit Repair Order" />
      {loading ? (
        <p>Loading...</p>
      ) : !order ? (
        <p>Order not found</p>
      ) : (
        <div className="order-form">
          <form onSubmit={handleSubmit}>

            <div className="form-group">
              <label htmlFor="date_in">Date In:</label>
              <span>{order.date_in ? new Date(order.date_in).toISOString().split('T')[0] : ''}</span>
            </div>

            <div className="form-group">
              <label htmlFor="customer_id">Customer:</label>
              <span>{order.customer?.name}</span>
            </div>

            <div className="form-group">
              <label htmlFor="vehicle_id">Vehicle:</label>
              <span>{order.vehicle?.license_plate}</span>
            </div>

            <div className="form-group">
              <label htmlFor="status">Status:</label>
              <select
                id="status"
                name="status"
                value={order.status}
                onChange={handleChange}
                disabled={loading}
                className="select-control"
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="labor_cost">Labor Cost:</label>
              <input
                id="labor_cost"
                type="number"
                name="labor_cost"
                value={order.labor_cost}
                onChange={handleChange}
                disabled={loading}
                step="0.01"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="date_expected_out">Expected Out Date:</label>
              <input
                id="date_expected_out"
                type="date"
                name="date_expected_out"
                value={order.date_expected_out ? new Date(order.date_expected_out).toISOString().split('T')[0] : ''}
                onChange={handleDateChange}
                disabled={loading}
              />
            </div>

            {parts.length > 0 && (
              <div className="parts-used">
                <h4>Parts Used</h4>
                <div className="add-part-section">
                  <select
                    style={{ marginTop: 10 }}
                    id="add-part"
                    name="add-part"
                    onChange={(e) => setNewPartId(e.target.value)}
                    disabled={loadingInventory || loading}
                    className="select-control"
                  >
                    <option value="">Select a part...</option>
                    {inventory.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.name} - ${item.final_price?.toFixed(2)}
                      </option>
                    ))}
                  </select>
                  <button
                    style={{ marginTop: 10 }}
                    className="button button--info"
                    onClick={handleAddPart}
                    disabled={loading || !newPartId}
                  >
                    Add Part
                  </button>
                </div>
                <table className="short-table">
                  <thead>
                    <tr>
                      <th>Part Name</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {parts.map((part) => (
                      <tr key={part.id}>
                        <td>{part.name}</td>
                        <td>${part.final_price?.toFixed(2)}</td>
                        <td>
                          <input
                            type="number"
                            value={part.quantity_used}
                            onChange={(e) => handleQuantityChange(part.id, e.target.value)}
                            min="1"
                            className="input-control"
                            disabled={loading}
                          />
                        </td>
                        <td>${(part.quantity_used * part.final_price).toFixed(2)}</td>
                        <td>
                          <button
                            className="button button--delete"
                            onClick={() => handleDeletePart(part.id)}
                            disabled={loading}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            <button type="submit" className="button button--success" disabled={loading}>
              Save Changes
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default RepairOrderEdit;
