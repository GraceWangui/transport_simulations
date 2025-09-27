from django.apps import AppConfig
"""
This module defines the configuration for the 'simulations' Django application.

Classes:
    SimulationsConfig: Configuration class for the 'simulations' app.
        - Sets the default auto field to 'BigAutoField' for model primary keys.
        - Specifies the app name as 'simulations'.
"""


class SimulationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simulations'
