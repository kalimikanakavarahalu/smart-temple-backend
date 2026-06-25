from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import json

from src.models.database import get_db
from src.models.entities import DarshanPermission, User, UserRole
from src.services.qr_service import generate_qr_base64
from src.agents.permission_agent import evaluate_darshan_request
from src.schemas.response import APIResponse, success_response, error_response
from src.middleware.dependencies import get_current_user, require_staff

router = APIRouter()

class DarshanRequest(BaseModel):
    date: datetime
    slot: str

class DarshanScan(BaseModel):
    qr_data_string: str

@router.get("/devotees", response_model=APIResponse)
async def get_devotees():
    """Stub endpoint for devotee app basics."""
    return success_response("Devotees endpoint ready.", [])

@router.post("/darshan/request", response_model=APIResponse)
def request_darshan_permission(req: DarshanRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Book Darshan and generate a QR Code. Devotee only (or anyone logged in)."""
    # 1. Agent evaluates the request
    evaluation = evaluate_darshan_request(current_user.id, req.date, current_user.role.value)
    
    status = evaluation["status"]
    qr_code_b64 = None
    
    # 2. If approved, generate QR
    if status == "approved":
        qr_data = json.dumps({"user_id": current_user.id, "date": str(req.date), "slot": req.slot})
        qr_code_b64 = generate_qr_base64(qr_data)
        
    # 3. Save to DB
    permission = DarshanPermission(
        user_id=current_user.id,
        date=req.date,
        slot=req.slot,
        status=status,
        qr_code=qr_code_b64
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    
    return success_response(
        "Darshan request processed",
        {
            "permission_status": status,
            "reason": evaluation["reason"],
            "permission_id": permission.id,
            "qr_code": qr_code_b64
        }
    )

@router.post("/darshan/scan", response_model=APIResponse)
def scan_darshan_qr(req: DarshanScan, db: Session = Depends(get_db), current_user: User = Depends(require_staff)):
    """Scan the QR code at the temple entrance. Staff only."""
    # Parse the JSON string stored in the QR code
    try:
        data = json.loads(req.qr_data_string)
        user_id = data.get("user_id")
        date_str = data.get("date")
    except Exception:
        return error_response("Invalid QR Code format")

    # Verify in DB
    permission = db.query(DarshanPermission).filter(
        DarshanPermission.user_id == user_id, 
        DarshanPermission.status == "approved"
    ).first()
    
    if not permission:
        return error_response("No approved darshan found for this QR")

    # Mark as 'used'
    permission.status = "completed"
    db.commit()

    return success_response("QR Code Verified. Devotee allowed to enter.")
