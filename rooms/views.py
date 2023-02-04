from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
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
                room = serializer.save(
                    owner=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        raise ParseError(
                            f"Amenity with id {amenity_pk} does not exist."
                        )
                    # Option1️⃣: Fail in silence...
                    # try:
                    #     amenity = Amenity.objects.get(pk=amenity_pk)
                    # except Amenity.DoesNotExist:
                    #     pass

                    # Option2️⃣: Delete room... (모델을 생성했다가 지우는 것... 다음 모델의 pk(id)가 밀리게 됨...)
                    # try:
                    #     amenity = Amenity.objects.get(pk=amenity_pk)
                    # except Amenity.DoesNotExist:
                    #     room.delete() 👈
                    #     raise ParseError(
                    #         f"Amenity with id {amenity_pk} does not exist."
                    #     )

                    # MANY TO MANY FIELD
                    # amenities = [...]
                    # for amenity in amenities:
                    #   room.amenities.add(amenity) .... add, remove....
                    room.amenities.add(amenity)
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

    def update(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


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
