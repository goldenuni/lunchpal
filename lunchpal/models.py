from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    cuisine = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    items = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.restaurant} - {self.date}"

    class Meta:
        ordering = ["-date"]
