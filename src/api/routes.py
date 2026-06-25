from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import json

from src.models.database import get_db
from src.models.entities import DarshanPermission, User
from src.services.qr_service import generate_qr_base64
from src.agents.permission_agent import evaluate_darshan_request

router = APIRouter()

class DarshanRequest(BaseModel):
    user_id: int
    date: datetime
    slot: str

@router.get("/devotees")
async def get_devotees():
    """Stub endpoint for devotee app basics."""
    return {"status": "success", "data": [], "message": "Devotees endpoint ready."}

@router.post("/darshan/request")
def request_darshan_permission(req: DarshanRequest, db: Session = Depends(get_db)):
    # 1. Fetch User to get role
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 2. Agent evaluates the request
    evaluation = evaluate_darshan_request(user.id, req.date, user.role.value)
    
    status = evaluation["status"]
    qr_code_b64 = None
    
    # 3. If approved, generate QR
    if status == "approved":
        qr_data = json.dumps({"user_id": user.id, "date": str(req.date), "slot": req.slot})
        qr_code_b64 = generate_qr_base64(qr_data)
        
    # 4. Save to DB
    permission = DarshanPermission(
        user_id=user.id,
        date=req.date,
        slot=req.slot,
        status=status,
        qr_code=qr_code_b64
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    
    return {
        "status": "success", 
        "permission_status": status,
        "reason": evaluation["reason"],
        "permission_id": permission.id,
        "qr_code": qr_code_b64
    }

@router.get("/assets/tracking")
async def get_asset_locations():
    """Stub endpoint for staff attendance and asset tracker."""
    return {"status": "success", "assets": [], "alerts": []}

@router.post("/donations")
async def make_donation():
    """Stub endpoint for digital donations processing."""
    return {"status": "success", "transaction_id": "tx_stub_123", "message": "Donation recorded on ledger."}

@router.get("/crowd/status")
async def get_crowd_status():
    """Stub endpoint for crowd video analytics and stampede warning."""
    return {"status": "success", "density_level": "normal", "alerts": []}
