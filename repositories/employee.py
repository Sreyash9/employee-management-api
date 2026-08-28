from sqlalchemy.orm import Session

from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary,
        joining_date=employee.joining_date,
        is_active=employee.is_active
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    db_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not db_employee:
        return None

    update_data = employee.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_employee, field, value)

    db.commit()
    db.refresh(db_employee)

    return db_employee


def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee:
        db.delete(employee)
        db.commit()

    return employee

def get_employee_by_email(db: Session, email: str):
    return db.query(Employee).filter(
        Employee.email == email
    ).first()