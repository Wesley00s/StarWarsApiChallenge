import functions_framework

from starwars_controller import StarWarsController
from starwars_service import StarWarsService

service = StarWarsService()
controller = StarWarsController(service)


@functions_framework.http
def hello_http(request):
    return controller.handle_request(request)
