from django.contrib import admin
from .models import Simulation, Run

# Register your models here.

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ("title", "mode", "is_baseline", "created_at")
    list_filter = ("mode", "is_baseline", "created_at")
    search_fields = ("title", "description")


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ("label", "simulation", "metric_name", "metric_value", "created_at")
    list_filter = ("metric_name", "created_at", "simulation")
    search_fields = ("label", "git_commit")
