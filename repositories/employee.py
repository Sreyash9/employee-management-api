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


def get_employees(
    db: Session,
    department: str | None = None,
    name: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Employee)

    if department:
        query = query.filter(
            Employee.department == department
        )

    if name:
        query = query.filter(
            Employee.name.ilike(f"%{name}%")
        )

    total = query.count()

    sort_columns = {
        "id": Employee.id,
        "name": Employee.name,
        "salary": Employee.salary,
        "joining_date": Employee.joining_date,
        "created_at": Employee.created_at
    }

    if sort_by not in sort_columns:
        sort_by = "id"

    sort_column = sort_columns[sort_by]

    if order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    offset = (page - 1) * page_size

    employees = query.offset(
        offset
    ).limit(
        page_size
    ).all()

    return employees, total


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