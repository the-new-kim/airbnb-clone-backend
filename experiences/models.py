from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="Korea")
    city = models.CharField(max_length=80, default="Seoul")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    perks = models.ManyToManyField(
        "experiences.Perk",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    name = models.CharField(max_length=150)
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
