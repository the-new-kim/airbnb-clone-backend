from django.contrib import admin
from .models import Experience, Perk
from categories.models import Category


# Register your models here.
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ExperienceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(
            kind="experiences"
        )
        return form

    list_display = (
        "name",
        "start",
        "end",
        "price",
    )
    list_filter = ("start", "end", "price")


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "details",
        "explanation",
    )
