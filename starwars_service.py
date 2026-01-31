import json
import math
from typing import List, Dict, Any, Optional

from model.films import Film
from model.person import Person
from model.planet import Planet
from model.specie import Specie
from model.starship import Starship
from model.vehicle import Vehicle
from swapi_client import SWAPIClient


class StarWarsService:
    def __init__(self, client: Optional[SWAPIClient] = None):
        self.client = client or SWAPIClient()


    def get_resource_by_id(self, resource_type: str, resource_id: int, base_url: str) -> dict[str, Any] | None:
        data = []
        if resource_type in ['people', 'person']:
            data = self.client.get_people()
        elif resource_type in ['planets', 'planet']:
            data = self.client.get_planets()
        elif resource_type in ['starships', 'starship']:
            data = self.client.get_starships()
        elif resource_type in ['films', 'film']:
            data = self.client.get_films()
        elif resource_type in ['species', 'specie']:
            data = self.client.get_species()
        elif resource_type in ['vehicles', 'vehicle']:
            data = self.client.get_vehicles()
        else:
            return None

        target_suffix = f"/{resource_id}/"

        found_item = next((item for item in data if item['url'].endswith(target_suffix)), None)

        if found_item:
            return self._replace_urls(found_item, base_url)

        return None


    @staticmethod
    def _replace_urls(data: Dict[str, Any], base_url: str) -> Dict[str, Any]:
        if not base_url:
            return data

        my_api_url = base_url.rstrip('/')

        json_str = json.dumps(data)

        new_json_str = json_str.replace("https://swapi.dev/api", my_api_url)
        new_json_str = new_json_str.replace("http://swapi.dev/api", my_api_url)

        return json.loads(new_json_str)

    def _paginate(self, data: List[Dict], page: int, size: int, base_url: str = "") -> Dict[str, Any]:
        total_items = len(data)
        total_pages = math.ceil(total_items / size)
        page = max(1, page)
        start_index = (page - 1) * size
        end_index = start_index + size

        paginated_items = data[start_index:end_index]

        result = {
            "data": paginated_items,
            "meta": {
                "current_page": page,
                "per_page": size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }

        return self._replace_urls(result, base_url)

    def _process_resource(
            self,
            data: List[Dict],
            filter_term: Optional[str],
            filter_field: str,
            sort_by: Optional[str],
            page: int,
            size: int,
            base_url: str
    ) -> Dict[str, Any]:

        if filter_term:
            data = [
                item for item in data
                if filter_term.lower() in item.get(filter_field, '').lower()
            ]

        if sort_by and data:
            if sort_by in data[0]:
                try:
                    data.sort(key=lambda x: x.get(sort_by, ""))
                except TypeError:
                    pass

        return self._paginate(data, page, size, base_url)

    def get_people(
            self,
            name_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Person]:

        data = self.client.get_people()

        return self._process_resource(
            data,
            name_filter,
            'name',
            sort_by,
            page,
            size,
            base_url
        )

    def get_planets(
            self,
            name_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Planet]:

        data = self.client.get_planets()

        return self._process_resource(
            data,
            name_filter,
            'name',
            sort_by,
            page,
            size,
            base_url
        )

    def get_starships(
            self,
            name_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Starship]:

        data = self.client.get_starships()

        return self._process_resource(
            data,
            name_filter,
            'name',
            sort_by,
            page,
            size,
            base_url
        )

    def get_films(
            self,
            title_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Film]:

        data = self.client.get_films()

        return self._process_resource(
            data, title_filter,
            'title',
            sort_by,
            page,
            size,
            base_url
        )

    def get_species(
            self,
            name_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Specie]:

        data = self.client.get_species()

        return self._process_resource(
            data, name_filter,
            'name',
            sort_by,
            page,
            size,
            base_url
        )

    def get_vehicles(
            self,
            name_filter: Optional[str] = None,
            sort_by: Optional[str] = None,
            page: int = 1,
            size: int = 10,
            base_url: str = ""
    ) -> Dict[str, Vehicle]:

        data = self.client.get_vehicles()

        return self._process_resource(
            data, name_filter,
            'name',
            sort_by,
            page,
            size,
            base_url
        )
