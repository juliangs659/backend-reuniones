from typing import Optional
from pydantic import Field
from app.models.base import MongoBaseModel, PyObjectId


class Client(MongoBaseModel):
    name: str = Field(..., index=True)
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    
    status: str = "active"
    notes: Optional[str] = None
    priority: str = "medium"
    
    tax_id: Optional[str] = None
    billing_email: Optional[str] = None
    payment_terms: Optional[int] = 30
    
    created_by_id: Optional[PyObjectId] = None
