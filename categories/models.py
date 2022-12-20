from django.db import models
from common.models import CommonModel

# Create your models here.
class Category(CommonModel):
    class CategoryChoices(models.TextChoices):
        ROOMS = ("rooms", "Rooms")
        EXPERIENCES = ("experiences", "Experiences")

    name = models.CharField(max_length=180, default="")
    kind = models.CharField(max_length=15, choices=CategoryChoices.choices)

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
