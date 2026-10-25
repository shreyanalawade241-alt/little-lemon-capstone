"""URL configuration for the Little Lemon project."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # User registration + token authentication (Djoser)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # Web pages and REST API
    path("", include("restaurant.urls")),
]
