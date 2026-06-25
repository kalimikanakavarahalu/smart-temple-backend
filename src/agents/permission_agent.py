import datetime

def evaluate_darshan_request(user_id: int, date: datetime.datetime, user_role: str) -> dict:
    """
    Rule-based AI Agent logic for Darshan permissions.
    In a real scenario, this would connect to the Crowd Analytics DB and check live slot capacity.
    """
    # Simple Rule 1: VIPs always get approved instantly
    if user_role == "vip":
        return {"status": "approved", "reason": "VIP auto-approval"}

    # Simple Rule 2: Check simulated capacity for the date
    # Let's assume week-ends are highly crowded and might get rejected or pending manual review
    if date.weekday() >= 5: # Saturday=5, Sunday=6
        return {"status": "pending", "reason": "High weekend capacity. Requires manual review."}

    # Default approval for regular days
    return {"status": "approved", "reason": "Slot available for normal days"}
