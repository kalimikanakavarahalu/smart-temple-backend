from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from src.models.database import get_db
from src.models.entities import Asset, Alert, User
from src.agents.asset_agent import analyze_asset_movement
from src.schemas.response import APIResponse, success_response, error_response
from src.middleware.dependencies import require_admin, require_staff

router = APIRouter()

class AssetCreate(BaseModel):
    name: str
    rfid_tag: str
    category: str
    current_location: str
    is_secure: bool = True

class RFIDScan(BaseModel):
    rfid_tag: str
    new_location: str
    scanned_by_staff_id: int

@router.post("/register", response_model=APIResponse)
def register_asset(asset: AssetCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Register a new asset with an RFID tag. Only Admin can register."""
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return success_response("Asset registered successfully", {"asset_id": db_asset.id})

@router.post("/simulator/scan", response_model=APIResponse)
def simulate_rfid_scan(scan: RFIDScan, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    """Simulator endpoint: When an RFID reader detects an asset moving to a new location. Staff/Admin only."""
    asset = db.query(Asset).filter(Asset.rfid_tag == scan.rfid_tag).first()
    if not asset:
        return error_response("Asset not found")
        
    staff = db.query(User).filter(User.id == scan.scanned_by_staff_id).first()
    if not staff:
        return error_response("Staff not found")

    # Update location
    asset.current_location = scan.new_location
    db.commit()

    # Pass to AI Agent for theft detection
    analysis = analyze_asset_movement(asset, scan.new_location, staff.id, db)
    
    return success_response(f"Asset {asset.name} moved to {scan.new_location}.", {"security_analysis": analysis})

@router.get("/alerts", response_model=APIResponse)
def get_security_alerts(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Get all unresolved security alerts (e.g. for the Admin Dashboard)."""
    alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    return success_response("Security alerts fetched successfully", {"alerts": alerts})
