from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer

User = get_user_model()


class ModelTests(TestCase):
    def test_menu_str(self):
        item = Menu.objects.create(title="IceCream", price=Decimal("80.00"), inventory=100)
        self.assertEqual(str(item), "IceCream : 80.00")

    def test_booking_str(self):
        booking = Booking.objects.create(
            name="Anna",
            no_of_guests=4,
            booking_date=datetime(2026, 11, 1, 19, 30, tzinfo=timezone.utc),
        )
        self.assertEqual(str(booking), "Anna - 2026-11-01 19:30")


class SerializerTests(TestCase):
    def test_menu_serializer_output(self):
        item = Menu.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=20)
        data = MenuSerializer(item).data
        self.assertEqual(data["title"], "Greek Salad")
        self.assertEqual(data["price"], "12.50")
        self.assertEqual(data["inventory"], 20)

    def test_negative_inventory_rejected(self):
        serializer = MenuSerializer(data={"title": "X", "price": "1.00", "inventory": -1})
        self.assertFalse(serializer.is_valid())
        self.assertIn("inventory", serializer.errors)


class PageTests(TestCase):
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")

    def test_about_page(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_menu_page_lists_items(self):
        Menu.objects.create(title="Bruschetta", price=Decimal("7.00"), inventory=10)
        response = self.client.get("/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bruschetta")


class MenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="chef", password="Str0ng!Pass#99")
        self.item = Menu.objects.create(title="Pasta", price=Decimal("15.00"), inventory=30)

    def authenticate(self):
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_anonymous_can_list_menu(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_anonymous_can_get_single_item(self):
        response = self.client.get(f"/api/menu/{self.item.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Pasta")

    def test_anonymous_cannot_create_item(self):
        response = self.client.post(
            "/api/menu/", {"title": "Soup", "price": "5.00", "inventory": 5}, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_authenticated_can_create_item(self):
        self.authenticate()
        response = self.client.post(
            "/api/menu/", {"title": "Soup", "price": "5.00", "inventory": 5}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 2)

    def test_authenticated_can_update_item(self):
        self.authenticate()
        response = self.client.put(
            f"/api/menu/{self.item.id}/",
            {"title": "Pasta", "price": "16.00", "inventory": 25},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.price, Decimal("16.00"))

    def test_authenticated_can_delete_item(self):
        self.authenticate()
        response = self.client.delete(f"/api/menu/{self.item.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Menu.objects.count(), 0)


class BookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="guest", password="Str0ng!Pass#99")
        self.payload = {
            "name": "Maria",
            "no_of_guests": 3,
            "booking_date": "2026-11-05T18:00:00Z",
        }

    def authenticate(self):
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_booking_requires_authentication(self):
        response = self.client.get("/api/booking/tables/")
        self.assertEqual(response.status_code, 401)

    def test_create_and_list_booking(self):
        self.authenticate()
        response = self.client.post("/api/booking/tables/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/booking/tables/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_booking(self):
        self.authenticate()
        booking = Booking.objects.create(
            name="Maria", no_of_guests=3, booking_date="2026-11-05T18:00:00Z"
        )
        response = self.client.patch(
            f"/api/booking/tables/{booking.id}/", {"no_of_guests": 6}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.no_of_guests, 6)

    def test_delete_booking(self):
        self.authenticate()
        booking = Booking.objects.create(
            name="Maria", no_of_guests=3, booking_date="2026-11-05T18:00:00Z"
        )
        response = self.client.delete(f"/api/booking/tables/{booking.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

    def test_zero_guests_rejected(self):
        self.authenticate()
        bad = dict(self.payload, no_of_guests=0)
        response = self.client.post("/api/booking/tables/", bad, format="json")
        self.assertEqual(response.status_code, 400)


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        response = self.client.post(
            "/auth/users/",
            {"username": "newuser", "password": "Str0ng!Pass#99"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/auth/token/login/",
            {"username": "newuser", "password": "Str0ng!Pass#99"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_token", response.json())

    def test_login_with_wrong_password_fails(self):
        User.objects.create_user(username="someone", password="Str0ng!Pass#99")
        response = self.client.post(
            "/auth/token/login/",
            {"username": "someone", "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_current_user_requires_token(self):
        response = self.client.get("/auth/users/me/")
        self.assertEqual(response.status_code, 401)
