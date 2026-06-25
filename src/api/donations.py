from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from src.models.database import get_db
from src.models.entities import Donation, User
from src.agents.donation_agent import analyze_donation, generate_mock_blockchain_hash

router = APIRouter()

class DonationRequest(BaseModel):
    user_id: int = None # Optional, can be anonymous
    amount: float
    category: str # e.g. "Annadanam", "Hundi", "Renovation"

@router.post("/process")
def process_donation(req: DonationRequest, db: Session = Depends(get_db)):
    """Mock Payment Gateway and Donation processing."""
    
    # 1. AI Agent checks for fraud / KYC
    analysis = analyze_donation(req.amount, req.user_id)
    if analysis["status"] == "flagged":
        raise HTTPException(status_code=400, detail=analysis["reason"])

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

    return {
        "status": "success",
        "message": "Donation processed successfully and recorded on E-Hundi.",
        "transaction_id": mock_tx_id,
        "ledger_hash": ledger_hash
    }

@router.get("/history/{user_id}")
def get_user_donations(user_id: int, db: Session = Depends(get_db)):
    """Fetch past donations for a devotee."""
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    return {"status": "success", "total_donations": len(donations), "data": donations}
