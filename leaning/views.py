from django.http import JsonResponse


def api_root(request):
    # API root endpoint - shows available endpoints
    return JsonResponse({
        'message': 'Lahore Car Rental API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/register',
                'login': '/api/login',
                'token_refresh': '/api/token/refresh/',
            },
            'vehicles': {
                'list_create': '/api/vehicles/',
                'detail_update_delete': '/api/vehicles/{id}/',
            },
            'bookings': {
                'list_create': '/api/bookings/',
                'detail': '/api/bookings/{id}/',
                'filters': '?from=YYYY-MM-DD&to=YYYY-MM-DD&status=confirmed',
            },
        },
        
    })

