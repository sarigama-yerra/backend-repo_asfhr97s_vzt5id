"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- Client -> "client" collection
- Invoice -> "invoice" collection
- Project -> "project" collection
- Task -> "task" collection
- Employee -> "employee" collection
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Core SaaS data models for a video production studio

class Client(BaseModel):
    name: str = Field(..., description="Organization or person name")
    contact_name: Optional[str] = Field(None, description="Primary contact person")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    website: Optional[str] = Field(None, description="Client website")
    industry: Optional[str] = Field(None, description="Industry or vertical")
    notes: Optional[str] = Field(None, description="Relationship notes or requirements")
    address: Optional[str] = Field(None, description="Mailing address")
    status: Literal["lead", "active", "inactive"] = Field("active", description="Lifecycle status")

class Employee(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Work email")
    role: Literal["producer", "editor", "designer", "pm", "finance", "other"] = Field("other")
    rate_hour: Optional[float] = Field(None, ge=0, description="Hourly rate in USD")
    skills: List[str] = Field(default_factory=list, description="Capabilities/skills")
    availability: Literal["available", "busy", "ooo"] = Field("available")
    active: bool = Field(True)

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    client_id: Optional[str] = Field(None, description="Client reference id")
    description: Optional[str] = Field(None)
    status: Literal["planning", "pre", "production", "post", "delivered", "archived"] = Field("planning")
    start_date: Optional[datetime] = Field(None)
    due_date: Optional[datetime] = Field(None)
    budget: Optional[float] = Field(None, ge=0)
    tags: List[str] = Field(default_factory=list)
    members: List[str] = Field(default_factory=list, description="Employee ids assigned")

class Task(BaseModel):
    project_id: str = Field(..., description="Parent project id")
    title: str
    description: Optional[str] = None
    assignee_id: Optional[str] = Field(None, description="Employee id")
    status: Literal["todo", "in_progress", "review", "done"] = Field("todo")
    priority: Literal["low", "medium", "high", "urgent"] = Field("medium")
    due_date: Optional[datetime] = None
    estimate_hours: Optional[float] = Field(None, ge=0)
    labels: List[str] = Field(default_factory=list)

class InvoiceItem(BaseModel):
    description: str
    quantity: float = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)

class Invoice(BaseModel):
    client_id: str
    project_id: Optional[str] = None
    number: Optional[str] = Field(None, description="Human-friendly invoice number")
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    currency: Literal["USD", "EUR", "GBP", "CAD", "AUD", "INR"] = "USD"
    items: List[InvoiceItem] = Field(default_factory=list)
    tax_rate: float = Field(0.0, ge=0, le=1, description="e.g. 0.07 for 7%")
    discount: float = Field(0.0, ge=0, description="Flat discount amount")
    status: Literal["draft", "sent", "paid", "overdue", "void"] = "draft"
    notes: Optional[str] = None

# Optional example models kept for reference; collections will still be created if used
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
