import { useEffect, useMemo, useState } from 'react';
import Header from '../Header';
import { getOrder } from '../../services/repairOrderApi';
import { getInventoryPartsByOrder } from '../../services/inventoryApi';
import { useNavigate, useParams } from 'react-router-dom';

const RepairOrderDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [parts, setParts] = useState([]);

  const partsTotal = useMemo(() => {
    return parts.reduce((total, part) => total + part.quantity_used * part.final_price, 0);
  }, [parts]);

  const total = useMemo(() => {
    return partsTotal + order?.labor_cost || 0;
  }, [partsTotal, order]);

  useEffect(() => {
    const fetchOrder = async () => {
      setLoading(true);
      const data = await getOrder(id);
      const parts = await getInventoryPartsByOrder(id);
      setOrder(data);
      setParts(parts);
      setLoading(false);
    };

    fetchOrder();
  }, [id]);

  return (
    <div>
      <Header title="Repair Order Details" />
      <div className="repair-order-details-container">
        {loading ? <p>Loading...</p> :
          !order ? <p>No order found.</p> :
            (
              <>
                <div className="repair-order-details">
                  <p><strong>Order ID:</strong> {order.id}</p>
                  <p><strong>Status:</strong> {order.status.replace(/_/g, ' ').toUpperCase()}</p>
                  <p><strong>Date In:</strong> {new Date(order.date_in).toLocaleDateString()}</p>
                  <p><strong>Date Expected Out:</strong> {order.date_expected_out ? new Date(order.date_expected_out).toLocaleDateString() : 'Not set'}</p>
                  <p><strong>Date Out:</strong> {order.date_out ? new Date(order.date_out).toLocaleDateString() : 'Not set'}</p>
                  <p><strong>Vehicle:</strong> <a href={`/vehicles/detail/${order.vehicle.id}`} className={order.vehicle.is_active ? '' : 'is-not-active'}>{order.vehicle.license_plate}</a></p>
                  <p><strong>Customer:</strong> <a href={`/customers/detail/${order.customer.id}`} className={order.customer.is_active ? '' : 'is-not-active'}>{order.customer.name}</a></p>
                  <p><strong>Labor Cost:</strong> ${order.labor_cost.toFixed(2)}</p>
                  <p><strong>Parts Cost:</strong> ${partsTotal.toFixed(2)}</p>
                  <p><strong>Total: ${total.toFixed(2)}</strong></p>
                </div>
                {order.status !== 'completed' && order.status !== 'cancelled' && (
                  <button
                    className="button button--edit"
                    onClick={() => navigate(`/repair-orders/edit/${order.id}`)}
                  >
                    Edit
                  </button>
                )}

                {parts.length > 0 && (
                  <div className="parts-used">
                    <h4>Parts Used</h4>
                    <table className="short-table">
                      <thead>
                        <tr>
                          <th>Part Name</th>
                          <th>Quantity</th>
                          <th>Price</th>
                          <th>Total</th>
                        </tr>
                      </thead>
                      <tbody>
                        {parts.map((part) => (
                          <tr key={part.id}>
                            <td>{part.name}</td>
                            <td>{part.quantity_used}</td>
                            <td>${part.final_price?.toFixed(2)}</td>
                            <td>${(part.quantity_used * part.final_price).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </>
            )}
      </div>
    </div>
  );
};

export default RepairOrderDetail;