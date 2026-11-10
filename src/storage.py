import json
import os
from pathlib import Path


def _path() -> Path:
    return Path(os.getenv("EMPLOYEES_FILE", "config/employees.json"))


def load_employees() -> list[dict]:
    path = _path()
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_employees(employees: list[dict]) -> None:
    _path().write_text(json.dumps(employees, indent=2))
