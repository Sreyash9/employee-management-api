# Employee Management API

A RESTful Employee Management API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Pydantic**.

The project provides complete employee CRUD operations together with advanced employee listing features including department filtering, name searching, sorting, pagination, pagination metadata, validation, duplicate-email handling, and HTTP error handling.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [API Endpoints](#api-endpoints)
- [Employee Object](#employee-object)
- [Create Employee](#create-employee)
- [Get Employees](#get-employees)
- [Filtering](#filtering)
- [Searching](#searching)
- [Sorting](#sorting)
- [Pagination](#pagination)
- [Pagination Response](#pagination-response)
- [Combining Query Parameters](#combining-query-parameters)
- [Get Employee by ID](#get-employee-by-id)
- [Update Employee](#update-employee)
- [Delete Employee](#delete-employee)
- [Validation](#validation)
- [Error Handling](#error-handling)
- [Database Configuration](#database-configuration)
- [Alembic Migrations](#alembic-migrations)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Development Workflow](#development-workflow)
- [Future Improvements](#future-improvements)
- [Security](#security)
- [Author](#author)
- [License](#license)

---

## Project Overview

The Employee Management API is a backend REST API for managing employee records.

Each employee contains information such as:

- Employee ID
- Name
- Email
- Department
- Salary
- Joining date
- Active/inactive status
- Creation timestamp
- Update timestamp

The API follows a layered architecture so that HTTP handling, business logic, database queries, models, and schemas remain separated.

---

## Features

### Employee CRUD

- Create an employee
- Retrieve all employees
- Retrieve an employee by ID
- Update an employee
- Delete an employee

### Employee Listing

The `GET /employees/` endpoint supports:

- Department filtering
- Name searching
- Sorting
- Pagination
- Pagination metadata
- Query parameter validation
- Combining multiple query parameters

### Error Handling

The application handles:

- Employee not found
- Duplicate employee email
- Invalid query parameters
- Invalid pagination values

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Alembic | Database schema migrations |
| Pydantic | Request and response validation |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |

---

# Architecture

The application follows a layered architecture:

```text
                    Client
                       |
                       v
              +----------------+
              |   API Layer    |
              |     api/       |
              +----------------+
                       |
                       v
              +----------------+
              | Service Layer  |
              |   services/    |
              +----------------+
                       |
                       v
              +----------------+
              | Repository     |
              |    Layer       |
              | repositories/  |
              +----------------+
                       |
                       v
              +----------------+
              | SQLAlchemy     |
              |    Models      |
              +----------------+
                       |
                       v
              +----------------+
              |  PostgreSQL    |
              +----------------+
```

### API Layer

Located in:

```text
api/
```

Responsible for:

- HTTP endpoints
- Query parameters
- Dependency injection
- HTTP exceptions
- Response models

### Service Layer

Located in:

```text
services/
```

Responsible for:

- Business logic
- Coordinating repository operations
- Application-level rules

### Repository Layer

Located in:

```text
repositories/
```

Responsible for:

- Database queries
- Filtering
- Searching
- Sorting
- Pagination
- CRUD database operations

### Model Layer

Located in:

```text
models/
```

Responsible for defining SQLAlchemy database models.

### Schema Layer

Located in:

```text
schemas/
```

Responsible for:

- Request validation
- Response validation
- Pydantic models

### Database Layer

Located in:

```text
db/
```

Responsible for:

- Database configuration
- SQLAlchemy engine
- Database sessions
- Connection management

---

# Project Structure

```text
Employee Management Api/
│
├── alembic/
│   ├── versions/
│   │   └── <migration files>
│   └── ...
│
├── api/
│   └── employee.py
│
├── db/
│   └── database.py
│
├── models/
│   └── employee.py
│
├── repositories/
│   └── employee.py
│
├── schemas/
│   └── employee.py
│
├── services/
│   └── employee.py
│
├── tests/
│
├── utils/
│   └── exceptions.py
│
├── .env
├── .gitignore
├── .securecodeignore
├── alembic.ini
├── main.py
├── README.md
└── requirements.txt
```

---

# Database Design

The application uses PostgreSQL.

The primary table is:

```text
employees
```

## Employee Table

| Column | Description |
|---|---|
| `id` | Unique employee ID |
| `name` | Employee name |
| `email` | Employee email |
| `department` | Employee department |
| `salary` | Employee salary |
| `joining_date` | Employee joining date |
| `is_active` | Whether the employee is active |
| `created_at` | Record creation timestamp |
| `updated_at` | Record update timestamp |

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/employees/` | Create an employee |
| `GET` | `/employees/` | Get employees |
| `GET` | `/employees/{employee_id}` | Get an employee by ID |
| `PUT` | `/employees/{employee_id}` | Update an employee |
| `DELETE` | `/employees/{employee_id}` | Delete an employee |

The `GET /employees/` endpoint also supports filtering, searching, sorting, and pagination.

---

# Employee Object

A typical employee object looks like:

```json
{
    "id": 1,
    "name": "Sreyash Naik",
    "email": "sreyash@example.com",
    "department": "IT",
    "salary": 50000,
    "joining_date": "2026-08-28",
    "is_active": true,
    "created_at": "2026-08-28T10:30:00",
    "updated_at": "2026-08-28T10:30:00"
}
```

---

# Create Employee

## Endpoint

```http
POST /employees/
```

## Request Body

```json
{
    "name": "Sreyash Naik",
    "email": "sreyash@example.com",
    "department": "IT",
    "salary": 50000,
    "joining_date": "2026-08-28",
    "is_active": true
}
```

## Successful Response

```text
200 OK
```

Example:

```json
{
    "id": 1,
    "name": "Sreyash Naik",
    "email": "sreyash@example.com",
    "department": "IT",
    "salary": 50000,
    "joining_date": "2026-08-28",
    "is_active": true,
    "created_at": "2026-08-28T10:30:00",
    "updated_at": "2026-08-28T10:30:00"
}
```

> The exact HTTP status depends on the current route configuration.

---

# Get Employees

## Endpoint

```http
GET /employees/
```

Returns employees from the database.

The endpoint supports:

- Filtering
- Searching
- Sorting
- Pagination

---

# Filtering

Employees can be filtered by department.

## Example

```http
GET /employees/?department=IT
```

This returns employees whose department is exactly:

```text
IT
```

Another example:

```http
GET /employees/?department=HR
```

returns employees from the HR department.

---

# Searching

Employees can be searched by name.

## Example

```http
GET /employees/?name=rahul
```

The name search uses a case-insensitive partial match.

For example, a search for:

```text
rahul
```

can match:

```text
Rahul
Rahul Sharma
Rahul Patil
Rohit Rahul
```

The repository uses SQLAlchemy's `ilike()` functionality for this search.

Conceptually, the database condition is:

```sql
WHERE name ILIKE '%rahul%'
```

---

# Sorting

Employees can be sorted using:

```text
sort_by
```

and:

```text
order
```

## Supported Sort Fields

```text
id
name
salary
joining_date
created_at
```

## Supported Sort Orders

```text
asc
desc
```

---

## Sort by Salary Ascending

```http
GET /employees/?sort_by=salary&order=asc
```

Example ordering:

```text
35000
45000
50000
60000
80000
```

---

## Sort by Salary Descending

```http
GET /employees/?sort_by=salary&order=desc
```

Example ordering:

```text
80000
60000
50000
45000
35000
```

---

## Sort by Name

```http
GET /employees/?sort_by=name&order=asc
```

This sorts employees alphabetically by name.

---

# Pagination

Pagination allows a large employee dataset to be returned in smaller groups.

Two query parameters are supported:

```text
page
page_size
```

## Example

```http
GET /employees/?page=1&page_size=5
```

This requests the first page with up to 5 employees.

The second page can be requested using:

```http
GET /employees/?page=2&page_size=5
```

---

## Pagination Calculation

The repository calculates the offset using:

```python
offset = (page - 1) * page_size
```

For example:

```text
page = 1
page_size = 5

offset = (1 - 1) * 5
offset = 0
```

For page 2:

```text
page = 2
page_size = 5

offset = (2 - 1) * 5
offset = 5
```

The query then applies:

```python
query.offset(offset).limit(page_size)
```

---

# Pagination Response

The employee listing endpoint returns pagination metadata.

Example:

```json
{
    "items": [
        {
            "id": 1,
            "name": "Sreyash Naik",
            "email": "sreyash@example.com",
            "department": "IT",
            "salary": 50000,
            "joining_date": "2026-08-28",
            "is_active": true,
            "created_at": "2026-08-28T10:30:00",
            "updated_at": "2026-08-28T10:30:00"
        }
    ],
    "total": 25,
    "page": 1,
    "page_size": 10,
    "total_pages": 3
}
```

## Response Fields

| Field | Description |
|---|---|
| `items` | Employees returned on the current page |
| `total` | Total employees matching the filters |
| `page` | Current page number |
| `page_size` | Number of employees requested per page |
| `total_pages` | Total number of available pages |

---

# Combining Query Parameters

Filtering, searching, sorting, and pagination can be combined.

## Example

```http
GET /employees/?department=IT&name=rahul&sort_by=salary&order=desc&page=1&page_size=5
```

This request means:

1. Filter employees by department `IT`
2. Search employee names containing `rahul`
3. Sort by salary
4. Sort in descending order
5. Return page 1
6. Return up to 5 employees

Conceptually, the SQL query is:

```sql
SELECT *
FROM employees
WHERE department = 'IT'
AND name ILIKE '%rahul%'
ORDER BY salary DESC
LIMIT 5
OFFSET 0;
```

For page 2, the offset becomes 5:

```sql
LIMIT 5
OFFSET 5;
```

---

# Get Employee by ID

## Endpoint

```http
GET /employees/{employee_id}
```

## Example

```http
GET /employees/1
```

If employee `1` exists, the employee object is returned.

If the employee does not exist:

```json
{
    "detail": "Employee not found"
}
```

with:

```text
404 Not Found
```

---

# Update Employee

## Endpoint

```http
PUT /employees/{employee_id}
```

## Example

```http
PUT /employees/1
```

Request body:

```json
{
    "salary": 60000,
    "department": "Engineering"
}
```

The update operation uses the employee update schema and supports updating supplied fields.

If the employee does not exist:

```text
404 Not Found
```

---

# Delete Employee

## Endpoint

```http
DELETE /employees/{employee_id}
```

## Example

```http
DELETE /employees/1
```

Successful response:

```json
{
    "message": "Employee deleted successfully"
}
```

If the employee does not exist:

```json
{
    "detail": "Employee not found"
}
```

---

# Validation

FastAPI and Pydantic are used for request and response validation.

## Page Validation

The `page` parameter has:

```python
page: int = Query(1, ge=1)
```

Therefore:

| Value | Result |
|---:|---|
| `1` | Valid |
| `5` | Valid |
| `100` | Valid |
| `0` | Invalid |
| `-1` | Invalid |

---

## Page Size Validation

The `page_size` parameter has:

```python
page_size: int = Query(10, ge=1, le=100)
```

Therefore:

| Value | Result |
|---:|---|
| `1` | Valid |
| `10` | Valid |
| `100` | Valid |
| `0` | Invalid |
| `101` | Invalid |

Invalid query parameters result in:

```text
422 Unprocessable Entity
```

---

# Sorting Validation

The API supports the following sorting fields:

```text
id
name
salary
joining_date
created_at
```

Valid:

```http
GET /employees/?sort_by=salary
```

Invalid:

```http
GET /employees/?sort_by=banana
```

The supported sorting orders are:

```text
asc
desc
```

Invalid values are rejected by query parameter validation.

---

# Error Handling

Custom application exceptions are stored in:

```text
utils/exceptions.py
```

One example is:

```text
EmployeeAlreadyExistsError
```

This exception is raised when an employee is created using an email that already exists.

The API converts this exception into:

```text
409 Conflict
```

Example:

```json
{
    "detail": "Employee with this email already exists"
}
```

## Common Status Codes

| Status Code | Meaning |
|---|---|
| `200` | Successful request |
| `404` | Employee not found |
| `409` | Duplicate employee/email |
| `422` | Request validation error |

---

# Database Configuration

Database configuration is handled through environment variables.

The `.env` file contains the database configuration.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5434/database_name
```

Use your actual PostgreSQL credentials and database name.

> Never commit database credentials or other secrets to source control.

---

# Alembic Migrations

Alembic is used to manage database schema changes.

Migration files are stored in:

```text
alembic/versions/
```

## Create a Migration

After modifying a SQLAlchemy model:

```bash
alembic revision --autogenerate -m "description of change"
```

Example:

```bash
alembic revision --autogenerate -m "add employee field"
```

## Apply Migrations

```bash
alembic upgrade head
```

## Check Current Migration

```bash
alembic current
```

## View Migration History

```bash
alembic history
```

---

# Installation

## 1. Clone the Project

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd "Employee Management Api"
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure PostgreSQL

Make sure PostgreSQL is installed and running.

Create the required database and configure the connection in `.env`.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5434/database_name
```

---

## 5. Run Database Migrations

From the project root:

```bash
alembic upgrade head
```

This applies all migrations and creates/updates the database schema.

---

# Running the Application

From the project root:

```bash
uvicorn main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

- View all endpoints
- View request parameters
- Submit request bodies
- Execute API calls
- Inspect responses
- Test query parameters
- Test validation

## ReDoc

FastAPI also provides ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Testing

Automated tests are maintained in:

```text
tests/
```

The test suite should cover the API's major behaviors.

## Employee Creation

- Create a valid employee
- Reject duplicate email

## Employee Retrieval

- Get all employees
- Get employee by ID
- Handle employee not found

## Employee Update

- Update an existing employee
- Handle non-existent employee

## Employee Deletion

- Delete an existing employee
- Handle non-existent employee

## Filtering

```http
GET /employees/?department=IT
```

## Searching

```http
GET /employees/?name=rahul
```

## Sorting

```http
GET /employees/?sort_by=salary&order=desc
```

## Pagination

```http
GET /employees/?page=1&page_size=5
```

## Combined Query

```http
GET /employees/?department=IT&name=rahul&sort_by=salary&order=desc&page=1&page_size=5
```

## Validation

Test invalid values such as:

```text
page=0
page=-1
page_size=0
page_size=101
sort_by=invalid
order=invalid
```

## Running Tests

Once tests are implemented:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

---

# Development Workflow

The recommended workflow is:

```text
1. Modify SQLAlchemy model
           |
           v
2. Create Alembic migration
           |
           v
3. Apply migration
           |
           v
4. Update Pydantic schemas
           |
           v
5. Update repository
           |
           v
6. Update service
           |
           v
7. Update API endpoint
           |
           v
8. Test using Swagger
           |
           v
9. Add/update automated tests
           |
           v
10. Commit changes
```

---

# Request Flow Example

For:

```http
GET /employees/?department=IT&sort_by=salary&order=desc&page=1&page_size=5
```

the request flows through the application like this:

```text
Client
  |
  v
api/employee.py
  |
  | Validate query parameters
  |
  v
services/employee.py
  |
  | Pass parameters
  |
  v
repositories/employee.py
  |
  +--> Apply department filter
  |
  +--> Apply name search if provided
  |
  +--> Count matching records
  |
  +--> Apply sorting
  |
  +--> Calculate offset
  |
  +--> Apply limit
  |
  v
PostgreSQL
  |
  v
Repository
  |
  v
Service
  |
  v
API
  |
  v
Pydantic Response
  |
  v
Client
```

---

# Query Parameters

The employee listing endpoint currently supports:

| Parameter | Default | Description |
|---|---|---|
| `department` | `None` | Filter employees by department |
| `name` | `None` | Search employee names |
| `sort_by` | `id` | Field used for sorting |
| `order` | `asc` | Sorting direction |
| `page` | `1` | Page number |
| `page_size` | `10` | Number of employees per page |

---

# Example Requests

## Get All Employees

```http
GET /employees/
```

## Get IT Employees

```http
GET /employees/?department=IT
```

## Search for Rahul

```http
GET /employees/?name=rahul
```

## Highest Salary First

```http
GET /employees/?sort_by=salary&order=desc
```

## First 10 Employees

```http
GET /employees/?page=1&page_size=10
```

## Second Page

```http
GET /employees/?page=2&page_size=10
```

## IT Employees Sorted by Salary

```http
GET /employees/?department=IT&sort_by=salary&order=desc
```

## Full Query

```http
GET /employees/?department=IT&name=rahul&sort_by=salary&order=desc&page=1&page_size=5
```

---

# Future Improvements

Potential improvements for the project include:

- Comprehensive automated test suite
- More advanced filtering
- Salary range filtering
- Joining-date range filtering
- Active/inactive employee filtering
- Multiple department filtering
- Database indexing for frequently searched fields
- Authentication and authorization
- JWT-based authentication
- Role-based access control
- Centralized exception handling
- Structured application logging
- API versioning
- Docker support
- Docker Compose for PostgreSQL
- Production deployment configuration
- CI/CD pipeline
- API rate limiting
- Dedicated test database
- Improved repository query optimization

---

# Security

Sensitive configuration should be stored in environment variables.

Do not commit:

```text
.env
```

or any database credentials to source control.

The repository includes:

```text
.gitignore
```

to help prevent sensitive files from being committed.

Before deploying the application, configure production secrets through the deployment environment rather than storing them directly in source code.

---

# Author

**Sreyash Naik**

Employee Management REST API project built to implement backend development concepts using:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic

---

# License

This project is currently intended for educational and development purposes.
