from datetime import datetime

from pydantic import BaseModel


class Planet(BaseModel):
    climate: str
    created: datetime
    diameter: str
    edited: datetime
    films: list[str]
    gravity: str
    name: str
    orbital_period: str
    population: str
    residents: list[str]
    rotation_period: str
    surface_water: str
    terrain: str
    url: str