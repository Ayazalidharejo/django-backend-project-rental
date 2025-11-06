from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Lahore Car Rental Backend API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/register',
                'login': '/api/login',
                'refresh_token': '/api/token/refresh/'
            },
            'vehicles': '/api/vehicles/',
            'bookings': '/api/bookings/',
            'admin': '/admin/'
        }
    })

