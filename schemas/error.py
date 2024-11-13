from pydantic import BaseModel, ValidationError

class ErrorSchema(BaseModel):
    """Defines how the errors will be returned"""
    error: str