import { useEffect, useState } from 'react';
import Header from '../Header';
import { getOrder, editOrder } from '../../services/repairOrderApi';
import { useNavigate, useParams } from 'react-router-dom';

const RepairOrderDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      setLoading(true);
      const data = await getOrder(id);
      setOrder(data);
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
                  <p><strong>Vehicle:</strong> {order.vehicle?.license_plate || 'N/A'}</p>
                  <p><strong>Customer:</strong> {order.customer?.name || 'N/A'}</p>
                  <p><strong>Labor Cost:</strong> ${order.labor_cost.toFixed(2)}</p>
                </div>
                {order.status !== 'completed' && order.status !== 'cancelled' && (
                  <button
                    className="button button--edit"
                    onClick={() => navigate(`/repair-orders/edit/${order.id}`)}
                  >
                    Edit
                  </button>
                )}
              </>
            )}
      </div>
    </div>
  );
};

export default RepairOrderDetail;