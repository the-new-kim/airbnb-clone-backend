from django.shortcuts import render
from django.http import HttpResponse
from rooms.models import Room

# Create your views here.


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {"rooms": rooms, "title": "This title comes from Django!!!"},
    )


def see_one_room(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        print(room)
        return render(request, "room_detail.html", {"room": room})
    except Room.DoesNotExist:
        print("NO ROOM FOUND")
        return render(request, "room_detail.html", {"not_found": True})
