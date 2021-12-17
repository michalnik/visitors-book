from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    class Cuisine(models.TextChoices):
        CZECH = "CZ", "Czech"
        GERMAN = "DE", "Germany"
        FRENCH = "FR", "French"
        GEORGIA = "GE", "Georgia"
        HAITI = "HT", "Haiti"
    name = models.CharField(max_length=80)
    place = models.CharField(max_length=80)
    type = models.CharField(
        max_length=2,
        choices=Cuisine.choices,
        default=Cuisine.FRENCH,
        db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visited_restaurants"
    )


class Visit(models.Model):
    class Evaluations(models.TextChoices):
        ONE = 1, "Terrible"
        TWO = 2, "Not so bad"
        THREE = 3, "Good"
        FOUR = 4, "Very well"
        FIVE = 5, "Fantastic"
    date = models.DateField(auto_now_add=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    evaluation = models.SmallIntegerField(choices=Evaluations.choices, default=Evaluations.THREE)
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
        related_name="visits"
    )
