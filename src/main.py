from fastapi import FastAPI, HTTPException

from src.models import Employee
from src.storage import load_employees, save_employees

app = FastAPI(title="Employee Service")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/employees")
def list_employees() -> list[dict]:
    return load_employees()


@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    for emp in load_employees():
        if emp["name"].lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail=f"Employee '{name}' not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee) -> dict:
    employees = load_employees()
    if any(e["name"].lower() == employee.name.lower() for e in employees):
        raise HTTPException(status_code=409, detail="Employee already exists")
    employees.append(employee.model_dump())
    save_employees(employees)
    return employee.model_dump()
