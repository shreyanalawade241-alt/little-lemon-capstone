LITTLE LEMON - Back-End Capstone (Django REST Framework + MySQL)
================================================================

WHAT IS INCLUDED
- Django serves static HTML pages (templates): /  /about/  /menu/
- MySQL database connection (see LittleLemon/settings.py)
- Menu API and Table Booking API (Django REST Framework)
- User registration + token authentication (Djoser)
- Unit tests (restaurant/tests.py)
- Works with the Insomnia REST client


SETUP
1. Create the MySQL database:
       CREATE DATABASE littlelemon;

2. Install dependencies (virtual environment recommended):
       pip install -r requirements.txt
   (If mysqlclient fails to install, see https://pypi.org/project/mysqlclient/
    for OS-specific build prerequisites.)

3. Set your MySQL credentials (defaults: user=root, password empty,
   host=127.0.0.1, port=3306, db=littlelemon):
       Windows (cmd):   set DB_PASSWORD=yourpassword
       Mac/Linux:       export DB_PASSWORD=yourpassword
   Optional variables: DB_NAME, DB_USER, DB_HOST, DB_PORT
   (or edit the DATABASES block in LittleLemon/settings.py directly)

   No MySQL handy? Run with SQLite instead by setting USE_SQLITE=1.

4. Create the tables and an admin user, then start the server:
       python manage.py migrate
       python manage.py createsuperuser
       python manage.py runserver

5. Run the unit tests:
       python manage.py test


API PATHS TO TEST (base URL: http://127.0.0.1:8000)
----------------------------------------------------
HTML pages (GET in browser)
 1  /                         Home page
 2  /about/                   About page
 3  /menu/                    Menu page (rendered from the database)

Registration & authentication (Djoser)
 4  POST /auth/users/                 Register. JSON body:
                                      {"username": "john", "password": "Str0ng!Pass#99"}
 5  POST /auth/token/login/           Login. Same JSON body. Returns {"auth_token": "..."}
 6  GET  /auth/users/me/              Current user (needs token header)
 7  POST /auth/token/logout/          Logout (needs token header)

   For every protected request add the header:
       Authorization: Token <auth_token>

Menu API
 8  GET    /api/menu/                 List all menu items (no login needed)
 9  POST   /api/menu/                 Create item (token required). JSON body:
                                      {"title": "Greek Salad", "price": "12.50", "inventory": 20}
10  GET    /api/menu/<id>/            Single item (no login needed)
11  PUT    /api/menu/<id>/            Update item (token required)
12  PATCH  /api/menu/<id>/            Partial update (token required)
13  DELETE /api/menu/<id>/            Delete item (token required)

Table Booking API (token required for all)
14  GET    /api/booking/tables/       List bookings
15  POST   /api/booking/tables/       Create booking. JSON body:
                                      {"name": "Maria", "no_of_guests": 3,
                                       "booking_date": "2026-11-05T18:00:00Z"}
16  GET    /api/booking/tables/<id>/  Single booking
17  PUT    /api/booking/tables/<id>/  Update booking
18  PATCH  /api/booking/tables/<id>/  Partial update
19  DELETE /api/booking/tables/<id>/  Delete booking

Other
20  /admin/                           Django admin site (superuser login)
21  POST /api-token-auth/             DRF token endpoint (username + password)


TESTING IN INSOMNIA - QUICK GUIDE
1. POST /auth/users/ to register, then POST /auth/token/login/ to get a token.
2. In any protected request, open the "Header" tab and add:
       Authorization  =  Token <your_token>
   (Use the word "Token", not "Bearer".)
3. Send requests to the paths above.
