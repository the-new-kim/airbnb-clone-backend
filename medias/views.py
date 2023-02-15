from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .serializers import PhotoSeriailzer

from .models import Photo

# Create your views here.


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
    def get(self,requestm,pk):
        photo = self.get_object(pk)
        serializer = PhotoSeriailzer(photo)
        return Response(serializer.data)

    def delete(self, request, pk):
        photo = self.get_object(pk)

        # if photo.room:
        #     if photo.room.owner != request.user:
        #         raise PermissionDenied
        # elif photo.experience:
        #     if photo.experience.host != request.user:
        #         raise PermissionDenied

        # 👆Before...👇After

        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()

        return Response(status=HTTP_200_OK)

