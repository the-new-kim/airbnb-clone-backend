from rest_framework import serializers

from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishlistSerializer(serializers.ModelSerializer):
    rooms = RoomListSerializer(read_only=True, many=True)
    # experiences =

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
