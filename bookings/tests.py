from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from vehicles.models import Vehicle
from .models import Booking
from .validators import validate_booking_dates


class BookingTests(TestCase):
    """Test cases for booking endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create a vehicle
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='ABC123'
        )
        
        self.bookings_url = '/api/bookings/'
        self.today = timezone.now().date()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after = self.today + timedelta(days=2)

    def test_create_booking_success(self):
        """Test successful booking creation"""
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(self.tomorrow),
            'end_date': str(self.day_after),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.vehicle, self.vehicle)
        self.assertGreater(booking.deposit_amount, 0)

    def test_create_booking_without_authentication(self):
        """Test booking creation without authentication"""
        self.client.credentials()  # Remove authentication
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(self.tomorrow),
            'end_date': str(self.day_after),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_overlapping_dates(self):
        """Test booking creation with overlapping dates"""
        # Create first booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow,
            end_date=self.day_after,
            status='confirmed'
        )
        
        # Try to create overlapping booking
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(self.tomorrow),
            'end_date': str(self.day_after),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already booked', str(response.data).lower())

    def test_create_booking_past_date(self):
        """Test booking creation with past date"""
        past_date = self.today - timedelta(days=1)
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(past_date),
            'end_date': str(self.tomorrow),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_end_before_start(self):
        """Test booking with end date before start date"""
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(self.day_after),
            'end_date': str(self.tomorrow),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_bookings(self):
        """Test listing bookings for authenticated user"""
        # Create bookings for both users
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow,
            end_date=self.day_after,
        )
        Booking.objects.create(
            user=self.other_user,
            vehicle=self.vehicle,
            start_date=self.tomorrow + timedelta(days=3),
            end_date=self.day_after + timedelta(days=3),
        )
        
        response = self.client.get(self.bookings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_bookings_with_date_filter(self):
        """Test listing bookings with date filters"""
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow,
            end_date=self.day_after,
        )
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow + timedelta(days=5),
            end_date=self.day_after + timedelta(days=5),
        )
        
        # Filter by from date
        response = self.client.get(f'{self.bookings_url}?from={self.tomorrow + timedelta(days=3)}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_booking_overlap_prevention(self):
        """Test that booking overlaps are prevented correctly"""
        # Create confirmed booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow,
            end_date=self.day_after,
            status='confirmed'
        )
        
        # Try overlapping booking (same dates)
        try:
            validate_booking_dates(self.tomorrow, self.day_after, self.vehicle)
            self.fail("Should have raised ValidationError")
        except Exception as e:
            self.assertIn('already booked', str(e).lower())
        
        # Try overlapping booking (partial overlap)
        try:
            validate_booking_dates(self.tomorrow, self.day_after + timedelta(days=1), self.vehicle)
            self.fail("Should have raised ValidationError")
        except Exception as e:
            self.assertIn('already booked', str(e).lower())

    def test_booking_deposit_calculation(self):
        """Test that deposit is calculated correctly"""
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(self.tomorrow),
            'end_date': str(self.day_after),
        }
        response = self.client.post(self.bookings_url, data, format='json')
        booking = Booking.objects.first()
        # Deposit should be 20% of (2 days * $50/day) = $20
        self.assertGreater(booking.deposit_amount, 0)
        self.assertEqual(booking.deposit_paid, False)

    def test_list_bookings_with_status_filter(self):
        """Test listing bookings filtered by status"""
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow,
            end_date=self.day_after,
            status='confirmed'
        )
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=self.tomorrow + timedelta(days=5),
            end_date=self.day_after + timedelta(days=5),
            status='cancelled'
        )
        
        response = self.client.get(f'{self.bookings_url}?status=confirmed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'confirmed')
