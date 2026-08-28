from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float
    joining_date: date
    is_active: bool = True


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = None
    joining_date: date | None = None
    is_active: bool | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: float
    joining_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int