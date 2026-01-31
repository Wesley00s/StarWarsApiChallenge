from datetime import datetime

from pydantic import BaseModel


class Starship(BaseModel):
    MGLT: str
    cargo_capacity: str
    consumables: str
    cost_in_credits: str
    created: datetime
    crew: str
    edited: datetime
    films: list[str]
    hyperdrive_rating: int
    length: str
    manufacturer: str
    max_atmosphering_speed: str
    model: str
    name: str
    passengers: str
    pilots: list[str]
    starship_class: str
    url: str
