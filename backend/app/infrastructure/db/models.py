import uuid
from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from app.domain.enums import RepairOrderStatus

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=True)

    vehicles = relationship("Vehicle", back_populates="customer")
    repair_orders = relationship("RepairOrder", back_populates="customer")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    license_plate = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="vehicles")
    repair_orders = relationship("RepairOrder", back_populates="vehicle")

class InventoryPart(Base):
    __tablename__ = "inventory_parts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    repair_order_parts = relationship("RepairOrderPart", back_populates="part")

class RepairOrder(Base):
    __tablename__ = "repair_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(RepairOrderStatus), default=RepairOrderStatus.PENDING, nullable=False)
    labor_cost = Column(Float, nullable=False)

    vehicle = relationship("Vehicle", back_populates="repair_orders")
    customer = relationship("Customer", back_populates="repair_orders")
    parts = relationship("RepairOrderPart", back_populates="repair_order")

class RepairOrderPart(Base):
    __tablename__ = "repair_order_parts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repair_order_id = Column(UUID(as_uuid=True), ForeignKey("repair_orders.id"), nullable=False)
    part_id = Column(UUID(as_uuid=True), ForeignKey("inventory_parts.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    repair_order = relationship("RepairOrder", back_populates="parts")
    part = relationship("InventoryPart", back_populates="repair_order_parts")
