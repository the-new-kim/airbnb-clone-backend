from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )


class CrerateBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        # Example:
        # Want:
        #   Checkin  = 03-10
        #   Checkout = 03-20

        # Existing❌:
        #   Checkin  = 03-15
        #   Checkout = 03-25

        # Existing❌:
        #   Checkin  = 03-05
        #   Checkout = 03-15

        # Existing✅:
        #   Checkin  = 03-25
        #   Checkout = 03-30

        # Existing✅:
        #   Checkin  = 03-01
        #   Checkout = 03-09

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some of those) dates are already taken."
            )

        return data

        # return super().validate(attrs)
