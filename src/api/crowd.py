from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.models.database import get_db
from src.agents.crowd_agent import analyze_crowd_density

router = APIRouter()

class CameraFeedSimulator(BaseModel):
    zone_name: str
    estimated_head_count: int

@router.post("/simulator/camera_feed")
def simulate_camera_feed(feed: CameraFeedSimulator, db: Session = Depends(get_db)):
    """Simulator endpoint: Receives fake head counts from a mocked CCTV camera."""
    
    analysis = analyze_crowd_density(feed.zone_name, feed.estimated_head_count, db)
    
    return {
        "status": "success",
        "zone": feed.zone_name,
        "head_count": feed.estimated_head_count,
        "ai_analysis": analysis
    }

@router.post("/evacuation")
def trigger_evacuation(zone_name: str):
    """Endpoint to broadcast evacuation routes to devotee mobile apps in a specific zone."""
    # In a real app, this would use WebSockets or Firebase Cloud Messaging (FCM)
    return {
        "status": "success",
        "message": f"Evacuation alert and dynamic exit routes broadcasted to all users in {zone_name}."
    }
