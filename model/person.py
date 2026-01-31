from datetime import datetime

from pydantic import BaseModel

class Person(BaseModel):
    birth_year: str
    created: datetime
    edited: datetime
    eye_color: str
    films: list[str]
    gender: str
    hair_color: str
    height: str
    homeworld: str
    mass: str
    name: str
    skin_color: str
    species: list[str]
    starships: list[str]
    url: str
    vehicles: list[str]

