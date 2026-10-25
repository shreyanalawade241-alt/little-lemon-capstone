from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"booking/tables", views.BookingViewSet, basename="booking")

urlpatterns = [
    # HTML pages
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu_page, name="menu-page"),
    # API
    path("api/menu/", views.MenuItemsView.as_view(), name="menu-items"),
    path("api/menu/<int:pk>/", views.SingleMenuItemView.as_view(), name="menu-item"),
    path("api/", include(router.urls)),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
]
