import functions_framework
from dotenv import load_dotenv

from starwars_controller import StarWarsController
from starwars_service import StarWarsService

load_dotenv()

service = StarWarsService()
controller = StarWarsController(service)


@functions_framework.http
def hello_http(request):
    return controller.handle_request(request)
