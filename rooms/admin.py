from django.contrib import admin
from .models import Room, Amenity
from categories.models import Category

# Register your models here.


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    print("HELOOOOOOOOOO")
    print(rooms)
    for room in rooms:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(kind="rooms")
        return form

    actions = (reset_prices,)

    list_display = (
        "name",
        "country",
        "price",
        "city",
        "rooms",
        "total_amenities",
        "rating",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
    )

    search_fields = (
        "name",
        "^price",
        "=owner__username",
    )

    def total_amenities(self, room):
        return room.amenities.count()

    # def total_amenities(self, room):
    #     print(room.anemities.count())
    #     return room.anemities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
