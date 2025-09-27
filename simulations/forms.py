from django import forms
from .models import Simulation, Run


"""
forms.py

This module defines Django ModelForm classes for the Simulation and Run models.

Classes:
    SimulationForm: 
        - A ModelForm for creating and updating Simulation instances.
        - Fields included: title, description, mode, is_baseline.

    RunForm:
        - A ModelForm for creating and updating Run instances.
        - Fields included: simulation, label, git_commit, co2_emissions.
"""



class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ["title", "description", "mode", "is_baseline"]

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ["simulation", "label", "git_commit", "co2_emissions"]
