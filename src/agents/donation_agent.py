import hashlib
from datetime import datetime

def analyze_donation(amount: float, user_id: int) -> dict:
    """
    AI Agent logic to detect suspicious donation activities.
    E.g., huge anonymous donations might need KYC verification.
    """
    if amount > 100000:
        return {
            "status": "flagged", 
            "reason": "Amount exceeds 1 Lakh. KYC Verification Required for anti-money laundering."
        }
    return {"status": "clear", "reason": "Normal transaction amount."}

def generate_mock_blockchain_hash(transaction_id: str, amount: float) -> str:
    """
    Simulates writing the donation to an E-Hundi Blockchain ledger.
    Returns a SHA-256 hash representing the block receipt.
    """
    raw_data = f"{transaction_id}-{amount}-{datetime.utcnow().isoformat()}"
    return hashlib.sha256(raw_data.encode()).hexdigest()
