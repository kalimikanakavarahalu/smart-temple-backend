from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from src.models.database import get_db
from src.models.entities import Asset, Alert, User
from src.agents.asset_agent import analyze_asset_movement

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

@router.post("/register")
def register_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """Register a new asset with an RFID tag."""
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return {"status": "success", "asset_id": db_asset.id}

@router.post("/simulator/scan")
def simulate_rfid_scan(scan: RFIDScan, db: Session = Depends(get_db)):
    """Simulator endpoint: When an RFID reader detects an asset moving to a new location."""
    asset = db.query(Asset).filter(Asset.rfid_tag == scan.rfid_tag).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    staff = db.query(User).filter(User.id == scan.scanned_by_staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    # Update location
    asset.current_location = scan.new_location
    db.commit()

    # Pass to AI Agent for theft detection
    analysis = analyze_asset_movement(asset, scan.new_location, staff.id, db)
    
    return {
        "status": "success", 
        "message": f"Asset {asset.name} moved to {scan.new_location}.",
        "security_analysis": analysis
    }

@router.get("/alerts")
def get_security_alerts(db: Session = Depends(get_db)):
    """Get all unresolved security alerts (e.g. for the Admin Dashboard)."""
    alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    return {"status": "success", "alerts": alerts}
