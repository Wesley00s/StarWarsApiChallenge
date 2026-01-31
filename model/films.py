from datetime import datetime

from pydantic import BaseModel


class Film(BaseModel):
    characters: list[str]
    created: datetime
    director: str
    edited: datetime
    episode_id: int
    opening_crawl: str
    planets: list[str]
    producer: str
    release_date: str
    species: list[str]
    starships: list[str]
    title: str
    url: str