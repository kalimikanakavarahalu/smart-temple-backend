from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.models.database import get_db
from src.models.entities import User
from src.agents.crowd_agent import analyze_crowd_density
from src.schemas.response import APIResponse, success_response, error_response
from src.middleware.dependencies import require_admin, require_staff

router = APIRouter()

class CameraFeedSimulator(BaseModel):
    zone_name: str
    estimated_head_count: int

@router.post("/simulator/camera_feed", response_model=APIResponse)
def simulate_camera_feed(feed: CameraFeedSimulator, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Simulator endpoint: Receives fake head counts from a mocked CCTV camera. Admin only."""
    
    analysis = analyze_crowd_density(feed.zone_name, feed.estimated_head_count, db)
    
    return success_response(
        "Camera feed analyzed successfully",
        {
            "zone": feed.zone_name,
            "head_count": feed.estimated_head_count,
            "ai_analysis": analysis
        }
    )

@router.post("/evacuation", response_model=APIResponse)
def trigger_evacuation(zone_name: str, current_user: User = Depends(require_staff)):
    """Endpoint to broadcast evacuation routes to devotee mobile apps in a specific zone. Admin/Staff only."""
    # In a real app, this would use WebSockets or Firebase Cloud Messaging (FCM)
    return success_response(
        "Evacuation triggered",
        {"details": f"Evacuation alert and dynamic exit routes broadcasted to all users in {zone_name}."}
    )
