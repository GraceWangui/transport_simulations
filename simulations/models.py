from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model() # Reference the user modelvs

class Simulation(models.Model):
    MODE_CHOICES = [
        ("road", "Road"),
        ("rail", "Rail"),
        ("maritime", "Maritime"),
        ("aviation", "Aviation"),
        ("multi", "Multi-modal"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default="road")
    author = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="simulations")
    author = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="runs")
    is_baseline = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self) -> str:
        return self.title

class Run(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name="runs")
    label = models.CharField(max_length=120)
    git_commit = models.CharField(max_length=40, unique=True, db_index=True, help_text="Short commit hash, e.g. a1b2c3d")
    co2_emissions = models.FloatField(help_text="Result in tonnes of CO₂")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.label} (CO₂={self.co2_emissions} t)"
