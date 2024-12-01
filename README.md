# Event API

This project implements a simplified Event Management API for an admin panel, supporting role-based access, event creation, and ticket purchases. The system uses Django REST Framework and JWT for authentication.

---

## Features

### User Roles:
1. **Admin**: Can create and manage events.
2. **User**: Can view events and purchase tickets.

### Functionalities:
- User registration with roles.
- JWT-based authentication for login and token refresh.
- Event management (create, list events).
- Ticket purchase with validation for availability.

---

## Installation

### Prerequisites:
- Python 3.8+
- PostgreSQL

### Steps:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EVENTAPI
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',  # or 'django.db.backends.mysql'
           'NAME': 'event_api_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication
1. **User Registration**:
   - `POST /api/register/`
   - Request Body:
     ```json
     {
         "username": "user1",
         "password": "password123",
         "role": "Admin"
     }
     ```

2. **Login to User**:
   - `POST /api/login/`
   - Request Body:
     ```json
     {
         "username": "user1",
         "password": "password123"
     }
     ```
   - Response:
     ```json
     {
         "access": "access_token",
         "refresh": "refresh_token"
     }
     ```

3. **Refresh Token**:
   - `POST /api/token/refresh/`
   - Request Body:
     ```json
     {
         "refresh": "refresh_token"
     }
     ```

### Events
1. **Get All Events**:
   - `GET /api/events/`
   - Authorization: Bearer `acess_token`

2. **Create Event**:
   - `POST /api/events/`
   - Authorization: Bearer `access_token`
   - Request Body:
     ```json
     {
         "name": "Music Festival",
         "date": "2024-12-25",
         "total_tickets": 1000
     }
     ```

### Ticket Purchase
1. **Purchase Tickets**:
   - `POST /api/events/{id}/purchase/`
   - Authorization: Bearer `access_token`
   - Request Body:
     ```json
     {
         "quantity": 2
     }
     ```

---

## SQL Query
To fetch the top 3 events by tickets sold:
```sql
SELECT id, name, date, total_tickets, tickets_sold
FROM events_event
ORDER BY tickets_sold DESC
LIMIT 3;
```

---

### Note:
Refer to the `curl` examples provided in the documentation for testing each endpoint.

---

