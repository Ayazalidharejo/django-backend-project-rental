# Lahore Car Rental Backend API

A Django REST Framework backend API for managing car rental operations, built for 1Now backend developer case study.

## About 1Now

**What 1Now Does:**
1Now builds comprehensive software solutions for independent car rental companies. The platform provides small to medium-sized car rental operators with the tools they need to manage their business digitally, including online booking systems, rental agreement management, calendar scheduling, and payment processing capabilities.

**Who It Serves:**
1Now serves independent car rental companies - businesses like LahoreCarRental.com that operate their own fleet of vehicles and need a complete digital solution to manage bookings, agreements, and payments without the complexity or cost of enterprise-level solutions.

**How This Backend Connects to LahoreCarRental.com:**
This backend API serves as the core data and business logic layer for LahoreCarRental.com's frontend. The frontend application would make HTTP requests to these endpoints to:
- Authenticate users and manage sessions using JWT tokens
- Allow fleet owners to manage their vehicle inventory (add, update, delete vehicles)
- Enable customers to browse available vehicles and create bookings
- Handle booking conflicts and prevent double-booking
- Process deposit payments (with mock Stripe integration structure)
- Filter and query bookings by date ranges and status

The frontend would consume these RESTful endpoints to build a complete user interface, handling all user interactions while the backend manages data persistence, validation, business rules, and security.



## Features

 **User Authentication**: JWT-based authentication with registration and login endpoints
 **Vehicle Management**: Full CRUD operations for vehicles (Create, Read, Update, Delete)
 **Booking Management**: Create and list bookings with overlap prevention
 **Input Validation**: Comprehensive validation for all inputs with clear error messages
 **Custom Validators**: Custom date and booking conflict validators
 **Query Filters**: Filter bookings by date range and status
 **Mock Stripe Integration**: Structure for deposit payment processing
 **Security**: JWT authentication with user-scoped data access
 **Testing**: Comprehensive unit tests for all modules



## Prerequisites

 Python 3.8 or higher
 pip (Python package manager)
 Virtual environment (recommended)


The API will be available at `http://localhost:8000/api/`

### Troubleshooting

**If you get `ERR_EMPTY_RESPONSE` error:**
1. Make sure virtual environment is activated: `.\venv\Scripts\Activate.ps1`
2. Check if server is running: `python manage.py runserver`
3. Make sure migrations are applied: `python manage.py migrate`
4. Check if static files are collected: `python manage.py collectstatic`
5. Try accessing: `http://127.0.0.1:8000/admin/` instead of `localhost`

**If admin panel doesn't load:**
- Create a superuser: `python manage.py createsuperuser`
- Then login at: `http://localhost:8000/admin/`

---

## All Available Routes

### Admin Panel
- `http://localhost:8000/admin/` - Django Admin Panel (requires superuser account)

### API Root
- `http://localhost:8000/` - API root endpoint (shows all available endpoints)

### Authentication Endpoints
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT tokens
- `POST /api/token/refresh/` - Refresh access token

### Vehicle Endpoints (JWT Required)
- `GET /api/vehicles/` - List all vehicles (user's vehicles only)
- `POST /api/vehicles/` - Create a new vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle (full update)
- `PATCH /api/vehicles/{id}/` - Update vehicle (partial update)
- `DELETE /api/vehicles/{id}/` - Delete a vehicle

### Booking Endpoints (JWT Required)
- `GET /api/bookings/` - List all bookings (user's bookings only)
  - Query Parameters:
    - `?from=YYYY-MM-DD` - Filter bookings from this date
    - `?to=YYYY-MM-DD` - Filter bookings up to this date
    - `?status=pending|confirmed|cancelled` - Filter by status
    - Example: `/api/bookings/?from=2024-02-01&status=confirmed`
- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking (full update)
- `PATCH /api/bookings/{id}/` - Update booking (partial update)
- `DELETE /api/bookings/{id}/` - Delete a booking

---

For detailed API documentation with request/response examples, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## Sample Requests & Responses

### 1. Register a User

**Request:**
```bash
POST http://localhost:8000/api/register
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

### 2. Login

**Request:**
```bash
POST http://localhost:8000/api/login
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

### 3. Create a Vehicle

**Request:**
```bash
POST http://localhost:8000/api/vehicles/
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

### 4. List Vehicles

**Request:**
```bash
GET http://localhost:8000/api/vehicles/
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

### 5. Create a Booking

**Request:**
```bash
POST http://localhost:8000/api/bookings/
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

### 6. List Bookings with Filters

**Request:**
```bash
GET http://localhost:8000/api/bookings/?from=2024-02-01&status=confirmed
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
      "status": "confirmed",
      "deposit_amount": "50.00",
      "deposit_paid": false,
      "created_at": "2024-01-15T10:40:00Z",
      "updated_at": "2024-01-15T10:40:00Z"
    }
  ]
}
```

---

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

Test coverage includes:
- User registration and authentication
- Vehicle CRUD operations
- Booking creation with overlap prevention
- Input validation and error handling
- Permission and authorization checks

---

## Project Structure

```
myweb/
├── authentication/          # User authentication app
│   ├── serializers.py     # User registration/login serializers
│   ├── views.py           # Register/login endpoints
│   ├── urls.py            # Authentication URL routing
│   └── tests.py           # Authentication tests
├── vehicles/               # Vehicle management app
│   ├── models.py          # Vehicle model
│   ├── serializers.py     # Vehicle serializers
│   ├── views.py           # Vehicle ViewSet
│   ├── urls.py            # Vehicle URL routing
│   ├── admin.py           # Admin interface
│   └── tests.py           # Vehicle tests
├── bookings/              # Booking management app
│   ├── models.py          # Booking model
│   ├── serializers.py     # Booking serializers
│   ├── views.py           # Booking ViewSet
│   ├── urls.py            # Booking URL routing
│   ├── validators.py      # Custom booking validators
│   ├── payments.py        # Mock Stripe integration
│   ├── admin.py           # Admin interface
│   └── tests.py           # Booking tests
├── leaning/               # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── API_DOCUMENTATION.md   # Detailed API documentation
```

---

## Assumptions

1. **User Model**: Using Django's built-in User model. In production, a custom user model might be preferred for additional fields.

2. **Vehicle Ownership**: Each vehicle has a single owner (user). The system assumes vehicles belong to fleet operators who manage their own inventory.

3. **Booking Model**: Bookings are created by users who may or may not be the vehicle owner. The system prevents overlapping bookings for the same vehicle.

4. **Deposit Calculation**: Deposits are calculated as 20% of the total rental cost, using a mock daily rate of $50/day. This is a placeholder - actual rates would come from vehicle or pricing models.

5. **Date Handling**: All dates are handled in UTC. The system prevents booking dates in the past.

6. **JWT Token Lifetime**: Access tokens expire after 1 hour, refresh tokens after 1 day. This can be adjusted in settings.

7. **Database**: Using SQLite for development. In production, PostgreSQL or MySQL would be recommended.

8. **Payment Processing**: The Stripe integration is a mock structure. Real implementation would require Stripe API keys and proper webhook handling.

9. **Error Messages**: All error messages are in English. Internationalization would be needed for multi-language support.

10. **Booking Status**: Bookings default to "pending" status. Status transitions would typically be managed through additional endpoints or admin actions.

---

## Security Considerations

- All endpoints except `/register` and `/login` require JWT authentication
- Users can only access their own vehicles and bookings
- Password validation follows Django's built-in validators
- License plates are normalized to prevent duplicates
- Booking overlap prevention prevents double-booking
- Input validation prevents invalid data entry

---

## Future Enhancements

- Email verification for user registration
- Password reset functionality
- Booking status management endpoints
- Payment webhook handling for Stripe
- Real-time availability calendar
- Vehicle images and additional metadata
- Pricing tiers and promotional codes
- Admin dashboard endpoints
- Rate limiting and throttling
- API versioning

---

## License

This project is part of a case study assignment for 1Now.

---

## Contact

For questions or issues, please refer to the project repository.

