from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # User registration endpoint
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        # Generate JWT tokens for the new user
        token = RefreshToken.for_user(new_user)
        return Response({
            'user': UserSerializer(new_user).data,
            'refresh': str(token),
            'access': str(token.access_token),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Handle user login
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if credentials are provided
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user:
        # Generate tokens for authenticated user
        token = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(token),
            'access': str(token.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
