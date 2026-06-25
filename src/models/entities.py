from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
import datetime
import enum
from .database import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    VIP = "vip"
    DEVOTEE = "devotee"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.DEVOTEE)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rfid_tag = Column(String, unique=True, index=True)
    category = Column(String) # e.g., keys, jewellery, pooja_items
    current_location = Column(String)
    is_secure = Column(Boolean, default=True)

class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Can be anonymous
    amount = Column(Float)
    category = Column(String) # Annadanam, Renovation, Hundi
    transaction_id = Column(String, unique=True)
    blockchain_hash = Column(String, nullable=True) # For E-Hundi ledger
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DarshanPermission(Base):
    __tablename__ = "darshan_permissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    slot = Column(String)
    qr_code = Column(String, unique=True)
    status = Column(String, default="pending") # pending, approved, scanned

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pooja_name = Column(String)
    date = Column(DateTime)
    status = Column(String, default="confirmed")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(String)
    severity = Column(String) # low, medium, high, critical
    source = Column(String) # e.g., crowd_agent, theft_agent
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
