"""Custom DRF exception handler for standardized error responses."""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'type': type(exc).__name__,
                'message': _extract_message(response.data),
                'details': response.data if isinstance(response.data, dict) else None,
            }
        }
        response.data = custom_data

    return response


def _extract_message(data):
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return data[0] if data else "Unknown error"
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        for key, value in data.items():
            if isinstance(value, list):
                return f"{key}: {value[0]}"
            return f"{key}: {value}"
    return "An error occurred"
