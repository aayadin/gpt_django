from functools import wraps

from rest_framework import status
from rest_framework.response import Response

import requests


def api_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = requests.get('https://api.openai.com/')
        if response.status_code == status.HTTP_421_MISDIRECTED_REQUEST:
            return func(*args, **kwargs)
        else:
            return Response(
                {'error': f'{response.status_code}'},
                response.status_code
            )
    return wrapper
