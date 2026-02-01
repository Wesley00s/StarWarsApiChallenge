import os
from flask import jsonify, Request
from typing import Tuple, Dict, Any
from starwars_service import StarWarsService


class StarWarsController:
    def __init__(self, service: StarWarsService):
        self.service = service

    def handle_request(self, request: Request) -> Tuple[Any, int, Dict[str, str]]:
        cors_headers = {
            'Access-Control-Allow-Origin': '*'
        }

        if request.method == 'OPTIONS':
            options_headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return '', 204, options_headers

        configured_base_url = os.environ.get('BASE_URL', '').rstrip('/')

        if configured_base_url:
            current_base_url = configured_base_url


        elif request.headers.get('X-Forwarded-Host'):
            forwarded_host = request.headers.get('X-Forwarded-Host')
            forwarded_proto = request.headers.get('X-Forwarded-Proto', 'https')
            current_base_url = f"{forwarded_proto}://{forwarded_host}"


        else:
            current_base_url = request.url_root.rstrip('/')

        path_segments = [p for p in request.path.strip('/').split('/') if p]

        resource_type = None
        resource_id = None

        if not path_segments:
            resource_type = request.args.get('type', 'people')

        elif len(path_segments) == 1:
            resource_type = path_segments[0]

        elif len(path_segments) == 2:
            resource_type = path_segments[0]
            try:
                resource_id = int(path_segments[1])
            except ValueError:
                return jsonify({'error': 'ID must be an integer'}), 400, cors_headers

        request_args = request.args
        filter_term = request_args.get('filter') or request_args.get('name')
        sort_by = request_args.get('sort')
        try:
            page = int(request_args.get('page', 1))
            size = int(request_args.get('size', 10))
        except ValueError:
            return jsonify({'error': 'Page and size must be integers'}), 400, cors_headers

        try:
            if resource_id:

                item = self.service.get_resource_by_id(resource_type, resource_id, current_base_url)
                if item:
                    return jsonify(item), 200, cors_headers
                else:
                    return jsonify({'error': 'Not Found'}), 404, cors_headers

            data = {}
            rt = resource_type.lower()

            if rt in ['people', 'person']:
                data = self.service.get_people(filter_term, sort_by, page, size, base_url=current_base_url)
            elif rt in ['planets', 'planet']:
                data = self.service.get_planets(filter_term, sort_by, page, size, base_url=current_base_url)
            elif rt in ['starships', 'starship']:
                data = self.service.get_starships(filter_term, sort_by, page, size, base_url=current_base_url)
            elif rt in ['films', 'film']:
                data = self.service.get_films(filter_term, sort_by, page, size, base_url=current_base_url)
            elif rt in ['species', 'specie']:
                data = self.service.get_species(filter_term, sort_by, page, size, base_url=current_base_url)
            elif rt in ['vehicles', 'vehicle']:
                data = self.service.get_vehicles(filter_term, sort_by, page, size, base_url=current_base_url)
            else:
                return jsonify({
                    'error': f'Resource type "{resource_type}" not supported.'
                }), 400, cors_headers

            return jsonify(data), 200, cors_headers

        except Exception as e:
            return jsonify({'error': str(e)}), 500, cors_headers
