from django.db import models
"""
Django models for transport simulations.

Classes:
    Simulation:
        Represents a transport simulation scenario.
        Fields:
            - title (str): Title of the simulation.
            - description (str): Optional description of the simulation.
            - mode (str): Mode of transport (road, rail, maritime, aviation, multi-modal).
            - author (User): Reference to the user who created the simulation.
            - is_baseline (bool): Indicates if this simulation is a baseline scenario.
            - created_at (datetime): Timestamp when the simulation was created.
        Meta:
            - ordering: Simulations are ordered by creation date (descending) and title.
        Methods:
            - __str__: Returns the simulation title.

    Run:
        Represents a single run or execution of a simulation.
        Fields:
            - simulation (Simulation): Reference to the associated simulation.
            - label (str): Label for the run.
            - git_commit (str): Unique git commit hash for reproducibility.
            - co2_emissions (float): CO₂ emissions result in tonnes.
            - author (User): Reference to the user who created the run.
            - created_at (datetime): Timestamp when the run was created.
        Meta:
            - ordering: Runs are ordered by creation date (descending).
        Methods:
            - __str__: Returns a string with the run label and CO₂ emissions.

Notes:
    - Uses Django's get_user_model for user references.
    - Models are designed for extensibility and tracking simulation results.
"""
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
    author = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="simulations",
    )
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
    author = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="runs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.label} (CO₂={self.co2_emissions} t)"
