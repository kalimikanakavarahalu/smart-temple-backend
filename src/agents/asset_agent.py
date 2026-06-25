from sqlalchemy.orm import Session
from src.models.entities import Asset, Alert

def analyze_asset_movement(asset: Asset, new_location: str, staff_id: int, db: Session) -> dict:
    """
    AI Agent logic to detect if an asset movement is a potential theft or unauthorized.
    In reality, this would use a pattern-matching model or predefined business rules.
    """
    allowed_locations_for_secure_items = ["Strong Room", "Main Sanctum", "Audit Room"]
    
    if asset.is_secure and new_location not in allowed_locations_for_secure_items:
        # Create a critical alert
        alert = Alert(
            title="CRITICAL: Unauthorized Secure Asset Movement",
            message=f"Secure asset '{asset.name}' (RFID: {asset.rfid_tag}) was moved to an unauthorized location: {new_location} by Staff ID: {staff_id}.",
            severity="critical",
            source="theft_agent"
        )
        db.add(alert)
        db.commit()
        return {"status": "alert_triggered", "severity": "critical", "message": "Unauthorized movement detected!"}
    
    # If safe, just return ok
    return {"status": "safe", "message": "Movement authorized."}
