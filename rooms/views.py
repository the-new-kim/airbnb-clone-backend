from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Room, Amenity
from .serializer import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from categories.models import Category


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):

        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():

                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")

                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except Category.DoesNotExist:
                    raise ParseError("Category does not exist.")

                # ONE TO ONE
                # owner = User.objects.get....
                # room.owener = owner
                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                except Exception:
                    raise ParseError("Amenity not found.")

                    # MANY TO MANY FIELD
                    # amenities = [...]
                    # for amenity in amenities:
                    #   room.amenities.add(amenity) .... add, remove....
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk=pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            # 1️⃣ Category
            if "category" in request.data:
                category_pk = request.data.get("category")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                    room.category = category
                except Category.DoesNotExist:
                    raise ParseError("Category does not exist.")

            # 2️⃣ Amenities
            if "amenities" in request.data:
                amenities = request.data.get("amenities")
                try:
                    room.amenities.clear()
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                except Exception:
                    raise ParseError("Amenity does not exist.")
            updated_room = serializer.save()
        return Response(RoomDetailSerializer(updated_room).data)

    def delete(self, request, pk):
        room = self.get_object(pk=pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(HTTP_204_NO_CONTENT)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)

        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(HTTP_204_NO_CONTENT)
