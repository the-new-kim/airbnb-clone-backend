from django.contrib import admin
from .models import Room, Amenity
from categories.models import Category

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(kind="rooms")
        return form

    list_display = (
        "name",
        "country",
        "city",
        "rooms",
        "total_amenities",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
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
