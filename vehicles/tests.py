from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Vehicle


class VehicleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        self.vehicles_url = '/api/vehicles/'

    def test_create_vehicle(self):
        """Test creating a new vehicle"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': 'LHR-123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.first().owner, self.user)

    def test_list_user_vehicles(self):
        """Test listing user's vehicles"""
        Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        Vehicle.objects.create(owner=self.user, make='Honda', model='Civic', year=2021, plate='LHR-456')
        
        other_user = User.objects.create_user(username='otheruser', password='pass123')
        Vehicle.objects.create(owner=other_user, make='Ford', model='Focus', year=2019, plate='LHR-789')
        
        response = self.client.get(self.vehicles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_vehicle(self):
        """Test updating a vehicle"""
        vehicle = Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        data = {'make': 'Honda', 'model': 'Civic', 'year': 2021, 'plate': 'LHR-456'}
        response = self.client.put(f'{self.vehicles_url}{vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.make, 'Honda')

    def test_delete_vehicle(self):
        """Test deleting a vehicle"""
        vehicle = Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        response = self.client.delete(f'{self.vehicles_url}{vehicle.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_vehicle_plate_normalization(self):
        """Test plate number normalization"""
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'plate': '  lhr-123  '
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vehicle = Vehicle.objects.first()
        self.assertEqual(vehicle.plate, 'LHR-123')

    def test_vehicle_unauthorized_access(self):
        """Test that users cannot access other users' vehicles"""
        other_user = User.objects.create_user(username='otheruser', password='pass123')
        vehicle = Vehicle.objects.create(owner=other_user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        response = self.client.get(f'{self.vehicles_url}{vehicle.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vehicle_partial_update(self):
        """Test partial update (PATCH) of a vehicle"""
        vehicle = Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        data = {'year': 2021}
        response = self.client.patch(f'{self.vehicles_url}{vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.year, 2021)

    def test_vehicle_duplicate_plate(self):
        """Test that duplicate plate numbers are not allowed"""
        Vehicle.objects.create(owner=self.user, make='Toyota', model='Corolla', year=2020, plate='LHR-123')
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'plate': 'LHR-123'
        }
        response = self.client.post(self.vehicles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
