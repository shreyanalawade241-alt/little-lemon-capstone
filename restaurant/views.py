from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


# ---------------------------------------------------------------------------
# Static HTML pages served by Django templates
# ---------------------------------------------------------------------------
def index(request):
    return render(request, "restaurant/index.html")


def about(request):
    return render(request, "restaurant/about.html")


def menu_page(request):
    items = Menu.objects.all().order_by("title")
    return render(request, "restaurant/menu.html", {"menu": items})


# ---------------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------------
class MenuItemsView(generics.ListCreateAPIView):
    """GET: anyone can list the menu.  POST: authenticated users only."""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET: anyone.  PUT/PATCH/DELETE: authenticated users only."""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """Table bookings - authentication required for every method."""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
