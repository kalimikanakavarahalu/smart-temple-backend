from fastapi import APIRouter

router = APIRouter()

@router.get("/devotees")
async def get_devotees():
    """Stub endpoint for devotee app basics."""
    return {"status": "success", "data": [], "message": "Devotees endpoint ready."}

@router.post("/darshan/request")
async def request_darshan_permission():
    """Stub endpoint for darshan permission requests."""
    return {"status": "success", "message": "Darshan permission requested.", "qr_code": "stub_qr_data"}

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
