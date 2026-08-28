from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse
)
from services import employee as employee_service
from utils.exceptions import EmployeeAlreadyExistsError

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        return employee_service.create_employee(
            db,
            employee
        )
    except EmployeeAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get("/", response_model=EmployeeListResponse)
def get_employees(
    department: str | None = None,
    name: str | None = None,
    sort_by: str = Query(
        "id",
        pattern="^(id|name|salary|joining_date|created_at)$"
    ),
    order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    employees, total = employee_service.get_employees(
        db,
        department,
        name,
        sort_by,
        order,
        page,
        page_size
    )

    total_pages = (
        total + page_size - 1
    ) // page_size

    return {
        "items": employees,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = employee_service.get_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    updated_employee = employee_service.update_employee(
        db,
        employee_id,
        employee
    )

    if not updated_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = employee_service.delete_employee(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }