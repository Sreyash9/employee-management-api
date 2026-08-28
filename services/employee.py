from sqlalchemy.orm import Session

from schemas.employee import EmployeeCreate, EmployeeUpdate
from repositories import employee as employee_repository
from utils.exceptions import EmployeeAlreadyExistsError

def create_employee(
    db: Session,
    employee: EmployeeCreate
):
    existing_employee = employee_repository.get_employee_by_email(
        db,
        employee.email
    )

    if existing_employee:
        raise EmployeeAlreadyExistsError(
            "Employee with this email already exists"
        )

    return employee_repository.create_employee(
        db,
        employee
    )


def get_employees(db: Session):
    return employee_repository.get_employees(db)


def get_employee(
    db: Session,
    employee_id: int
):
    return employee_repository.get_employee(
        db,
        employee_id
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    return employee_repository.update_employee(
        db,
        employee_id,
        employee
    )


def delete_employee(
    db: Session,
    employee_id: int
):
    return employee_repository.delete_employee(
        db,
        employee_id
    )