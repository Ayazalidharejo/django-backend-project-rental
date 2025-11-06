from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, timedelta
from vehicles.models import Vehicle
from .models import Booking


class BookingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        self.bookings_url = '/api/bookings/'
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            make='Toyota',
            model='Corolla',
            year=2020,
            plate='LHR-123'
        )

    def test_create_booking(self):
        """Test creating a new booking"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.status, 'pending')

    def test_booking_overlap_prevention(self):
        """Test that overlapping bookings are prevented"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        # Create first booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date,
            status='confirmed'
        )
        
        # Try to create overlapping booking
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date + timedelta(days=1)),
            'end_date': str(end_date + timedelta(days=1))
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_past_date_validation(self):
        """Test that past dates are not allowed"""
        start_date = date.today() - timedelta(days=1)
        end_date = date.today()
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_booking_end_before_start_validation(self):
        """Test that end date must be after start date"""
        start_date = date.today() + timedelta(days=3)
        end_date = date.today() + timedelta(days=1)
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_bookings(self):
        """Test listing user's bookings"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        response = self.client.get(self.bookings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get('results', [])), 1)

    def test_booking_date_filter(self):
        """Test filtering bookings by date range"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date
        )
        filter_date = str(start_date + timedelta(days=5))
        response = self.client.get(f'{self.bookings_url}?from={filter_date}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_status_filter(self):
        """Test filtering bookings by status"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date,
            status='confirmed'
        )
        response = self.client.get(f'{self.bookings_url}?status=confirmed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', [])
        if results:
            self.assertEqual(results[0]['status'], 'confirmed')

    def test_booking_deposit_calculation(self):
        """Test that deposit is calculated correctly"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=4)  # 5 days total
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.first()
        # 5 days * $50/day * 0.20 = $50
        self.assertEqual(float(booking.deposit_amount), 50.00)

    def test_booking_cancelled_overlap_allowed(self):
        """Test that cancelled bookings don't prevent new bookings"""
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        
        # Create cancelled booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date=start_date,
            end_date=end_date,
            status='cancelled'
        )
        
        # Should be able to create new booking for same dates
        data = {
            'vehicle': self.vehicle.id,
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
        response = self.client.post(self.bookings_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
