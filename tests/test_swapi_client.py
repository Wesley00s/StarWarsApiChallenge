import pytest
from unittest.mock import MagicMock
from swapi_client import SWAPIClient


@pytest.fixture
def client():
    return SWAPIClient()


def test_get_all_pages_pagination_logic(client, mocker):
    mock_response_page_1 = MagicMock()
    mock_response_page_1.json.return_value = {
        "results": [{"name": "Luke Skywalker"}],
        "next": "https://swapi.dev/api/people/?page=2"
    }
    mock_response_page_1.raise_for_status.return_value = None

    mock_response_page_2 = MagicMock()
    mock_response_page_2.json.return_value = {
        "results": [{"name": "C-3PO"}],
        "next": None
    }
    mock_response_page_2.raise_for_status.return_value = None

    mock_http_get = mocker.patch.object(client.client, 'get', side_effect=[
        mock_response_page_1,
        mock_response_page_2
    ])

    people = client.get_people()

    assert len(people) == 2
    assert people[0]['name'] == "Luke Skywalker"
    assert people[1]['name'] == "C-3PO"
    assert mock_http_get.call_count == 2


def test_get_films_single_page(client, mocker):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"title": "A New Hope"}, {"title": "Empire Strikes Back"}],
        "next": None
    }

    mock_http_get = mocker.patch.object(client.client, 'get', return_value=mock_response)
    films = client.get_films()

    assert len(films) == 2
    assert films[0]['title'] == "A New Hope"
    mock_http_get.assert_called_once()


@pytest.mark.parametrize("method_name, expected_endpoint", [
    ("get_people", "people"),
    ("get_planets", "planets"),
    ("get_starships", "starships"),
    ("get_films", "films"),
    ("get_species", "species"),
    ("get_vehicles", "vehicles"),
])
def test_all_endpoints_routing(client, mocker, method_name, expected_endpoint):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": [], "next": None}

    mock_get = mocker.patch.object(client.client, 'get', return_value=mock_response)

    method_to_call = getattr(client, method_name)
    method_to_call()

    expected_url = f"https://swapi.dev/api/{expected_endpoint}/"
    mock_get.assert_called_with(expected_url)
