import httpx
from typing import List, Dict, Any

from model.films import Film
from model.person import Person
from model.planet import Planet
from model.specie import Specie
from model.starship import Starship
from model.vehicle import Vehicle


class SWAPIClient:
    BASE_URL = "https://swapi.dev/api"

    def __init__(self):
        self.client = httpx.Client(timeout=10.0)

    def _get_all_pages(self, endpoint: str) -> List[Dict[str, Any]]:
        results = []
        next_url = f"{self.BASE_URL}/{endpoint}/"

        while next_url:
            response = self.client.get(next_url)
            response.raise_for_status()
            data = response.json()

            results.extend(data['results'])
            next_url = data['next']

        return results

    def get_people(self) -> List[Dict[str, Person]]:
        return self._get_all_pages("people")

    def get_planets(self) -> List[Dict[str, Planet]]:
        return self._get_all_pages("planets")

    def get_starships(self) -> List[Dict[str, Starship]]:
        return self._get_all_pages("starships")

    def get_films(self) -> List[Dict[str, Film]]:
        return self._get_all_pages("films")

    def get_species(self) -> List[Dict[str, Specie]]:
        return self._get_all_pages("species")

    def get_vehicles(self) -> List[Dict[str, Vehicle]]:
        return self._get_all_pages("vehicles")
