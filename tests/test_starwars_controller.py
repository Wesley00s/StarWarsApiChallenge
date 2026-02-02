import pytest
from unittest.mock import MagicMock
from flask import Flask
from starwars_controller import StarWarsController

app = Flask(__name__)


@pytest.fixture
def mock_service():
    service = MagicMock()

    success_return = {
        "data": [{"name": "Test Item"}],
        "meta": {"page": 1}
    }

    service.get_people.return_value = success_return
    service.get_planets.return_value = success_return
    service.get_starships.return_value = success_return
    service.get_films.return_value = success_return
    service.get_species.return_value = success_return
    service.get_vehicles.return_value = success_return
    service.get_resource_by_id.return_value = {"name": "Luke Skywalker", "url": "..."}

    return service


@pytest.fixture
def controller(mock_service):
    return StarWarsController(service=mock_service)


def test_handle_request_success(controller, mock_service):
    with app.test_request_context('/?type=people&filter=luke'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 200

        mock_service.get_people.assert_called_with(
            'luke',
            None,
            1,
            10,
            base_url='http://localhost',
            film_id=None
        )


def test_cors_options_request(controller):
    with app.test_request_context('/', method='OPTIONS'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 204
        assert headers['Access-Control-Allow-Methods'] == 'GET'


def test_validation_error_page_size(controller):
    with app.test_request_context('/?type=people&page=two'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 400
        assert 'integers' in response.json['error']


def test_resource_not_supported(controller):
    with app.test_request_context('/?type=wookies'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 400
        assert 'not supported' in response.json['error']


def test_internal_server_error(controller, mock_service):
    mock_service.get_people.side_effect = Exception("Critical Failure")

    with app.test_request_context('/?type=people'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 500
        assert response.json['error'] == "Critical Failure"


def test_filter_name_fallback(controller, mock_service):
    with app.test_request_context('/?type=people&name=Yoda'):
        from flask import request

        controller.handle_request(request)

        mock_service.get_people.assert_called_with(
            'Yoda',
            None,
            1,
            10,
            base_url='http://localhost',
            film_id=None
        )


def test_handle_request_with_film_id(controller, mock_service):
    with app.test_request_context('/?type=people&film_id=1'):
        from flask import request

        response, status_code, headers = controller.handle_request(request)

        assert status_code == 200
        mock_service.get_people.assert_called_with(
            None,
            None,
            1,
            10,
            base_url='http://localhost',
            film_id=1
        )


@pytest.mark.parametrize("resource_type, service_method", [
    ('planets', 'get_planets'),
    ('planet', 'get_planets'),
    ('starships', 'get_starships'),
    ('starship', 'get_starships'),
    ('films', 'get_films'),
    ('film', 'get_films'),
    ('species', 'get_species'),
    ('specie', 'get_species'),
    ('vehicles', 'get_vehicles'),
    ('vehicle', 'get_vehicles'),
])
def test_routing_logic(controller, mock_service, resource_type, service_method):
    with app.test_request_context(f'/?type={resource_type}'):
        from flask import request

        response, status, _ = controller.handle_request(request)

        assert status == 200
        getattr(mock_service, service_method).assert_called_once()


def test_get_by_id_routing(controller, mock_service):
    with app.test_request_context('/people/1'):
        from flask import request

        response, status, _ = controller.handle_request(request)

        assert status == 200
        mock_service.get_resource_by_id.assert_called_with('people', 1, 'http://localhost')
