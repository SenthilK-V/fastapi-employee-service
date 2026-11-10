from pydantic import BaseModel, Field, field_validator


class Employee(BaseModel):
    name: str
    salary: float = Field(gt=0)
    department: str = "General"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        return v
