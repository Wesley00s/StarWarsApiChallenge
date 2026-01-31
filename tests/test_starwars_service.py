import pytest
from unittest.mock import MagicMock
from starwars_service import StarWarsService


@pytest.fixture
def mock_client():
    client = MagicMock()

    client.get_people.return_value = [
        {"name": "Leia Organa", "height": "150"},
        {"name": "Luke Skywalker", "height": "172"},
        {"name": "Darth Vader", "height": "202"},
        {"name": "Han Solo", "height": "180"}
    ]

    client.get_films.return_value = [
        {"title": "A New Hope", "episode_id": 4},
        {"title": "The Empire Strikes Back", "episode_id": 5},
        {"title": "Return of the Jedi", "episode_id": 6}
    ]

    client.get_planets.return_value = [
        {"name": "Tatooine", "climate": "arid"},
        {"name": "Alderaan", "climate": "temperate"},
        {"name": "Hoth", "climate": "frozen"}
    ]

    client.get_starships.return_value = [
        {"name": "X-wing", "model": "T-65 X-wing"},
        {"name": "Millennium Falcon", "model": "YT-1300 light freighter"}
    ]

    client.get_species.return_value = [
        {"name": "Human", "classification": "mammal"},
        {"name": "Droid", "classification": "artificial"},
        {"name": "Wookiee", "classification": "mammal"}
    ]

    client.get_vehicles.return_value = [
        {"name": "Snowspeeder", "model": "t-47 airspeeder"},
        {"name": "Imperial Speeder Bike", "model": "74-Z speeder bike"}
    ]

    return client


@pytest.fixture
def service(mock_client):
    return StarWarsService(client=mock_client)


def test_get_people_filter_and_sort(service):
    response = service.get_people(name_filter="skywalker", sort_by="name")
    results = response['data']

    assert len(results) == 1
    assert results[0]['name'] == "Luke Skywalker"


def test_get_people_sort_logic(service):
    response = service.get_people(sort_by="name")
    results = response['data']

    assert results[0]['name'] == "Darth Vader"
    assert results[1]['name'] == "Han Solo"
    assert results[2]['name'] == "Leia Organa"
    assert results[3]['name'] == "Luke Skywalker"


def test_get_people_pagination(service):
    result = service.get_people(page=2, size=1)

    assert result['meta']['current_page'] == 2
    assert result['meta']['total_items'] == 4
    assert len(result['data']) == 1
    assert result['data'][0]['name'] == "Luke Skywalker"


def test_get_films_filter_by_title(service):
    response = service.get_films(title_filter="Empire", sort_by="title")
    results = response['data']

    assert len(results) == 1
    assert results[0]['title'] == "The Empire Strikes Back"


def test_get_planets_logic(service):
    response = service.get_planets(sort_by="name")
    results = response['data']

    assert results[0]['name'] == "Alderaan"
    assert len(results) == 3


def test_get_starships_simple(service):
    response = service.get_starships()
    assert len(response['data']) == 2
    assert response['meta']['total_items'] == 2


def test_get_species_logic(service):
    response = service.get_species(sort_by="name")
    results = response['data']

    assert len(results) == 3
    assert results[0]['name'] == "Droid"
    assert results[1]['name'] == "Human"


def test_get_vehicles_logic(service):
    response = service.get_vehicles()
    assert len(response['data']) == 2
    assert response['data'][0]['name'] == "Snowspeeder"


def test_safe_sort_invalid_key(service):
    response = service.get_people(sort_by="midichlorians")
    results = response['data']

    assert len(results) == 4
    assert results[0]['name'] == "Leia Organa"


def test_empty_search_result(service):
    response = service.get_people(name_filter="Spock")

    assert len(response['data']) == 0
    assert response['meta']['total_items'] == 0
    assert response['meta']['total_pages'] == 0
