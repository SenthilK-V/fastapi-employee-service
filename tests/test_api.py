import json

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    data = tmp_path / "employees.json"
    data.write_text(
        json.dumps([{"name": "Asha", "salary": 85000, "department": "Engineering"}])
    )
    monkeypatch.setenv("EMPLOYEES_FILE", str(data))
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_employees(client):
    r = client.get("/employees")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_employee_success(client):
    r = client.get("/employees/Asha")
    assert r.status_code == 200
    assert r.json()["name"] == "Asha"


def test_get_employee_not_found(client):
    assert client.get("/employees/Ravi").status_code == 404


def test_create_employee_success(client):
    r = client.post("/employees", json={"name": "Ravi", "salary": 60000})
    assert r.status_code == 201
    assert client.get("/employees/Ravi").status_code == 200


def test_create_employee_invalid_salary(client):
    r = client.post("/employees", json={"name": "Ravi", "salary": -5})
    assert r.status_code == 422


def test_create_employee_empty_name(client):
    r = client.post("/employees", json={"name": "   ", "salary": 5000})
    assert r.status_code == 422


def test_create_employee_duplicate(client):
    r = client.post("/employees", json={"name": "Asha", "salary": 1000})
    assert r.status_code == 409
