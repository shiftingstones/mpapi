"""A module that defines the Starship data type."""

from pydantic import BaseModel, Field, ConfigDict


class Starship(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    name: str
    model: str
    class_: str = Field(alias="class")  # alias since class is a reserved word
    cargo_capacity: int
    max_crew: int
    max_passengers: int
    hyperdrive_rating: float
