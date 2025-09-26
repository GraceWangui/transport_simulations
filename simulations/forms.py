from django import forms
from .models import Simulation, Run

class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ["title", "description", "mode", "is_baseline"]

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ["simulation", "label", "git_commit", "co2_emissions"]
