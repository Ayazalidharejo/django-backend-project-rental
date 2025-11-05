from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Vehicle


class VehicleTests(TestCase):
    """Test cases for vehicle endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.vehicles_url = '/api/vehicles/'

    def test_create_vehicle_success(self):
        """Test successful vehicle creation"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': 'ABC123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        vehicle = Vehicle.objects.first()
        self.assertEqual(vehicle.owner, self.user)
        self.assertEqual(vehicle.make, 'Toyota')

    def test_create_vehicle_without_authentication(self):
        """Test vehicle creation without authentication"""
        self.client.credentials()  # Remove authentication
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': 'ABC123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user_vehicles(self):
        """Test listing vehicles for authenticated user"""
        # Create vehicles for both users
        Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='ABC123')
        Vehicle.objects.create(owner=self.other_user, make='Honda', model='Civic', year=2021, plate='XYZ789')
        
        response = self.client.get(self.vehicles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')

    def test_update_vehicle_success(self):
        """Test successful vehicle update"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'plate': 'ABC123'
        }
        response = self.client.put(f'{self.vehicles_url}{vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.make, 'Honda')

    def test_update_other_user_vehicle(self):
        """Test updating vehicle owned by another user"""
        vehicle = Vehicle.objects.create(
            owner=self.other_user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'plate': 'ABC123'
        }
        response = self.client.put(f'{self.vehicles_url}{vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vehicle_success(self):
        """Test successful vehicle deletion"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        response = self.client.delete(f'{self.vehicles_url}{vehicle.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_delete_other_user_vehicle(self):
        """Test deleting vehicle owned by another user"""
        vehicle = Vehicle.objects.create(
            owner=self.other_user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        response = self.client.delete(f'{self.vehicles_url}{vehicle.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vehicle_duplicate_plate(self):
        """Test creating vehicle with duplicate license plate"""
        Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'plate': 'ABC123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_year_range(self):
        """Test vehicle year validation"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 1800,  # Invalid year
            'plate': 'ABC123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vehicle_serializer_plate_normalization(self):
        """Test that license plate is normalized to uppercase"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': 'abc123'  # Lowercase
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vehicle = Vehicle.objects.first()
        self.assertEqual(vehicle.plate, 'ABC123')
