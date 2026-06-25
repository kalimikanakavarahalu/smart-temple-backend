from typing import Any, Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None

def success_response(message: str, data: Any = None) -> dict:
    return {"success": True, "message": message, "data": data, "errors": None}

def error_response(message: str, errors: Any = None) -> dict:
    return {"success": False, "message": message, "data": None, "errors": errors}
