# api/views.py
from django.http import JsonResponse

def handle_initial_route(request):
    """
    Returns a JSON response similar to the Go code.
    """
    data = {
        "message": "Welcome to go api laaaa",
        "data": "restart gareko by django"
    }
    return JsonResponse(data)  # This automatically sets the content type to application/json
