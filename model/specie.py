from datetime import datetime

from pydantic import BaseModel


class Specie(BaseModel):
    average_height: str
    average_lifespan: str
    classification: str
    created: datetime
    designation: str
    edited: datetime
    eye_colors: str
    films: list[str]
    hair_colors: str
    homeworld: str
    language: str
    name: str
    people: list[str]
    skin_colors: str
    url: str