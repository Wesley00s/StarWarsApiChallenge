from datetime import datetime

from pydantic import BaseModel


class Vehicle(BaseModel):
    cargo_capacity: str
    consumables: str
    cost_in_credits: str
    created: datetime
    crew: str
    edited: datetime
    films: list[str]
    length: str
    manufacturer: str
    max_atmosphering_speed: str
    model: str
    name: str
    passengers: str
    pilots: list[str]
    url: str
    vehicle_class: str
