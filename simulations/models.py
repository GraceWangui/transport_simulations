from django.db import models

# Create your models here.

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
    is_baseline = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self) -> str:
        return self.title


class Run(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name="runs")
    label = models.CharField(max_length=120)
    git_commit = models.CharField(max_length=40, help_text="Short commit hash, e.g. a1b2c3d")
    params_json = models.JSONField(blank=True, null=True)
    metric_name = models.CharField(max_length=40, default="score")
    metric_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.label} ({self.metric_name}={self.metric_value})"
