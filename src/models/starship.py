from pydantic import BaseModel, Field


class Starship(BaseModel):
    name: str
    model: str
    class_: str = Field(alias="class")
    cargo_capacity: int
    max_crew: int
    max_passengers: int
