from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from src.models.database import get_db
from src.models.entities import Donation, User, UserRole
from src.agents.donation_agent import analyze_donation, generate_mock_blockchain_hash
from src.schemas.response import APIResponse, success_response, error_response
from src.middleware.dependencies import get_current_user

router = APIRouter()

class DonationRequest(BaseModel):
    user_id: int = None # Optional, can be anonymous
    amount: float
    category: str # e.g. "Annadanam", "Hundi", "Renovation"

@router.post("/process", response_model=APIResponse)
def process_donation(req: DonationRequest, db: Session = Depends(get_db)):
    """Mock Payment Gateway and Donation processing."""
    
    # 1. AI Agent checks for fraud / KYC
    analysis = analyze_donation(req.amount, req.user_id)
    if analysis["status"] == "flagged":
        return error_response(analysis["reason"])

    # 2. Mock Payment Gateway processing (always succeeds)
    mock_tx_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"

    # 3. Blockchain Ledger Entry (Mock)
    ledger_hash = generate_mock_blockchain_hash(mock_tx_id, req.amount)

    # 4. Save to DB
    donation = Donation(
        user_id=req.user_id,
        amount=req.amount,
        category=req.category,
        transaction_id=mock_tx_id,
        blockchain_hash=ledger_hash
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)

    return success_response(
        "Donation processed successfully and recorded on E-Hundi.",
        {
            "transaction_id": mock_tx_id,
            "ledger_hash": ledger_hash
        }
    )

@router.get("/history/{user_id}", response_model=APIResponse)
def get_user_donations(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch past donations for a devotee."""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        return error_response("You don't have permission to view this history.")
        
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    return success_response(
        "Donations fetched successfully",
        {
            "total_donations": len(donations),
            "donations": donations
        }
    )
