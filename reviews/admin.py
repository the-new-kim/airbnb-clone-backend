from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Bad"),
            ("good", "Good"),
        ]

    def queryset(self, request, reviews):
        word = self.value()

        if word:
            if word == "good":
                return reviews.filter(rating__gte=3)
            elif word == "bad":
                return reviews.filter(rating__lt=3)
        else:
            return reviews


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )
