import uuid
from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from app.domain.enums import RepairOrderStatus
from datetime import datetime, timezone

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    vehicles = relationship("Vehicle", back_populates="customer", lazy="select")
    repair_orders = relationship("RepairOrder", back_populates="customer", lazy="select")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    license_plate = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    customer = relationship("Customer", back_populates="vehicles", lazy="select")
    repair_orders = relationship("RepairOrder", back_populates="vehicle", lazy="select")

class InventoryPart(Base):
    __tablename__ = "inventory_parts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    final_price = Column(Float, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    repair_order_parts = relationship("RepairOrderPart", back_populates="part", lazy="select")

class RepairOrder(Base):
    __tablename__ = "repair_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(RepairOrderStatus), default=RepairOrderStatus.PENDING, nullable=False)
    labor_cost = Column(Float, nullable=False)
    date_in = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    date_expected_out = Column(DateTime, nullable=True)
    date_out = Column(DateTime, nullable=True)
    total_cost_repair = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)

    vehicle = relationship("Vehicle", back_populates="repair_orders", lazy="select")
    customer = relationship("Customer", back_populates="repair_orders", lazy="select")
    parts = relationship("RepairOrderPart", back_populates="repair_order", lazy="select")

class RepairOrderPart(Base):
    __tablename__ = "repair_order_parts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repair_order_id = Column(UUID(as_uuid=True), ForeignKey("repair_orders.id"), nullable=False)
    part_id = Column(UUID(as_uuid=True), ForeignKey("inventory_parts.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)

    repair_order = relationship("RepairOrder", back_populates="parts", lazy="select")
    part = relationship("InventoryPart", back_populates="repair_order_parts", lazy="select")
