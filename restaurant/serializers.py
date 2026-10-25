from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "title", "price", "inventory"]

    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "name", "no_of_guests", "booking_date"]

    def validate_no_of_guests(self, value):
        if value < 1:
            raise serializers.ValidationError("At least one guest is required.")
        return value
