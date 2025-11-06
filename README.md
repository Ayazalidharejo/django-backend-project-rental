# Lahore Car Rental Backend API

A Django REST Framework backend API for managing car rental operations, built for 1Now backend developer case study.

## About 1Now

**What 1Now Does:**
1Now builds software solutions for independent car rental companies. The platform helps small to medium-sized car rental operators manage their business digitally with online booking systems, rental agreements, calendar scheduling, and payment processing.

**Who It Serves:**
1Now serves independent car rental companies like LahoreCarRental.com that operate their own fleet and need a digital solution to manage bookings, agreements, and payments.

**How This Backend Connects to LahoreCarRental.com:**
This backend API provides the data layer for LahoreCarRental.com's frontend. The frontend uses these endpoints to:
- Authenticate users with JWT tokens
- Manage vehicle inventory (add, update, delete vehicles)
- Browse vehicles and create bookings
- Prevent double-booking conflicts
- Process deposit payments (mock Stripe integration)
- Filter bookings by date and status

The frontend makes HTTP requests to these endpoints while the backend handles data storage, validation, and security.

## Features

- User Authentication: JWT-based authentication with registration and login endpoints
- Vehicle Management: Full CRUD operations for vehicles (Create, Read, Update, Delete)
- Booking Management: Create and list bookings with overlap prevention
- Input Validation: Validation for all inputs with error messages
- Custom Validators: Custom date and booking conflict validators
- Query Filters: Filter bookings by date range and status
- Mock Stripe Integration: Structure for deposit payment processing
- Security: JWT authentication with user-scoped data access
- Testing: Unit tests for all modules (24 tests total)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd django-backend-project-rental
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (for admin panel)
```bash
python manage.py createsuperuser
```
Follow the prompts:
- Username: (enter your username, e.g., `admin`)
- Email: (enter your email, e.g., `admin@example.com`)
- Password: (enter a strong password)
- Password (again): (confirm password)

### 6. Run the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`
The Admin Panel will be available at `http://localhost:8000/admin/`

## API Endpoints

### Authentication

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "User registered successfully"
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Login successful"
}
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Vehicles

All vehicle endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### Create Vehicle
```http
POST /api/vehicles/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "plate": "LHR-123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "owner": 1,
  "owner_username": "john_doe",
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "plate": "LHR-123",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### List Vehicles
```http
GET /api/vehicles/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "owner": 1,
    "owner_username": "john_doe",
    "make": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "plate": "LHR-123",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Update Vehicle
```http
PUT /api/vehicles/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "make": "Honda",
  "model": "Civic",
  "year": 2021,
  "plate": "LHR-456"
}
```

**Response (200):**
```json
{
  "message": "Vehicle updated successfully",
  "data": {
    "id": 1,
    "owner": 1,
    "owner_username": "john_doe",
    "make": "Honda",
    "model": "Civic",
    "year": 2021,
    "plate": "LHR-456",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
}
```

#### Delete Vehicle
```http
DELETE /api/vehicles/{id}/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Vehicle deleted successfully"
}
```

### Bookings

All booking endpoints require JWT authentication.

#### Create Booking
```http
POST /api/bookings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "vehicle": 1,
  "start_date": "2024-02-01",
  "end_date": "2024-02-05"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "vehicle": 1,
  "vehicle_details": {
    "id": 1,
    "make": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "plate": "LHR-123"
  },
  "start_date": "2024-02-01",
  "end_date": "2024-02-05",
  "status": "pending",
  "deposit_amount": "50.00",
  "deposit_paid": false,
  "created_at": "2024-01-15T10:40:00Z",
  "updated_at": "2024-01-15T10:40:00Z"
}
```

#### List Bookings
```http
GET /api/bookings/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_username": "john_doe",
      "vehicle": 1,
      "vehicle_details": {
        "id": 1,
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "plate": "LHR-123"
      },
      "start_date": "2024-02-01",
      "end_date": "2024-02-05",
      "status": "pending",
      "deposit_amount": "50.00",
      "deposit_paid": false,
      "created_at": "2024-01-15T10:40:00Z",
      "updated_at": "2024-01-15T10:40:00Z"
    }
  ]
}
```

#### Filter Bookings

Filter by date range:
```http
GET /api/bookings/?from=2024-02-01&to=2024-02-28
Authorization: Bearer <access_token>
```

Filter by status:
```http
GET /api/bookings/?status=confirmed
Authorization: Bearer <access_token>
```

Combine filters:
```http
GET /api/bookings/?from=2024-02-01&status=confirmed
Authorization: Bearer <access_token>
```

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test authentication
python manage.py test vehicles
python manage.py test bookings
```

**Test Coverage:**
- Authentication: 6 tests (registration, login, validation)
- Vehicles: 6 tests (CRUD operations, authorization, validation)
- Bookings: 12 tests (creation, overlap prevention, date validation, filters)

**Total: 24 tests** - All passing

## Project Structure

```
django-backend-project-rental/
├── authentication/          # User authentication app
│   ├── serializers.py      # User registration/login serializers
│   ├── views.py            # Register/login endpoints
│   ├── urls.py             # Authentication URL routing
│   └── tests.py            # Authentication tests (6 tests)
├── vehicles/                # Vehicle management app
│   ├── models.py           # Vehicle model
│   ├── serializers.py      # Vehicle serializers
│   ├── views.py            # Vehicle ViewSet
│   ├── urls.py             # Vehicle URL routing
│   ├── admin.py            # Admin interface
│   └── tests.py            # Vehicle tests (6 tests)
├── bookings/                # Booking management app
│   ├── models.py           # Booking model
│   ├── serializers.py      # Booking serializers
│   ├── views.py            # Booking ViewSet
│   ├── urls.py             # Booking URL routing
│   ├── validators.py        # Custom booking validators
│   ├── payments.py         # Mock Stripe integration
│   ├── admin.py            # Admin interface
│   └── tests.py            # Booking tests (12 tests)
├── rental_backend/          # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore patterns
```

## Assumptions

1. User Model: Using Django's built-in User model. Custom user model can be added later if needed.

2. Vehicle Ownership: Each vehicle has one owner. Vehicles belong to fleet operators.

3. Booking Model: Users create bookings. System prevents overlapping bookings for same vehicle.

4. Deposit Calculation: 20% of rental cost, using $50/day mock rate. Can be updated later.

5. Date Handling: Dates in UTC. Past dates not allowed.

6. JWT Token Lifetime: Access tokens expire after 1 hour, refresh tokens after 1 day.

7. Database: SQLite for development. PostgreSQL or MySQL recommended for production.

8. Payment Processing: Mock Stripe integration. Real implementation needs API keys and webhooks.

9. Error Messages: All in English. Can add internationalization later.

10. Booking Status: Defaults to "pending". Status changes via endpoints or admin.

## Security

- JWT authentication required for all endpoints except `/register` and `/login`
- Users can only access their own vehicles and bookings
- Password validation uses Django's built-in validators
- License plates normalized to prevent duplicates
- Booking overlap prevention blocks double-booking
- Input validation prevents invalid data

## Bonus Features

- Booking Overlap Prevention: Prevents double-booking for overlapping dates
- Mock Stripe Integration: Structure for deposit payments (`bookings/payments.py`)
- Custom Validators: Date and booking conflict validators (`bookings/validators.py`)
- Query Filters: Filter bookings by date range and status

## Future Enhancements

- Email verification
- Password reset
- Booking status management
- Stripe payment webhooks
- Availability calendar
- Vehicle images
- Pricing tiers
- Admin dashboard
- Rate limiting
- API versioning

## License

This project is part of a case study assignment for 1Now.

## Contact

For questions or issues, please refer to the project repository.

