from sqlalchemy.orm import Session
from src.models.entities import Alert

def analyze_crowd_density(zone_name: str, head_count: int, db: Session) -> dict:
    """
    AI Agent logic to detect overcrowding and issue stampede warnings.
    """
    MAX_SAFE_CAPACITY = 500
    WARNING_THRESHOLD = 400

    if head_count > MAX_SAFE_CAPACITY:
        # Generate Stampede Warning Alert
        alert = Alert(
            title=f"CRITICAL: STAMPEDE WARNING in {zone_name}",
            message=f"Head count ({head_count}) exceeded safe capacity ({MAX_SAFE_CAPACITY}). Initiate evacuation protocol immediately.",
            severity="critical",
            source="crowd_agent"
        )
        db.add(alert)
        db.commit()
        return {
            "status": "danger",
            "density_level": "critical",
            "message": "Stampede risk! Evacuation required."
        }
    
    elif head_count > WARNING_THRESHOLD:
        return {
            "status": "warning",
            "density_level": "high",
            "message": "Approaching maximum capacity. Stop incoming queues."
        }
        
    return {
        "status": "safe",
        "density_level": "normal",
        "message": "Crowd is within safe limits."
    }
