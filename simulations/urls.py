from django.urls import path
from . import views

urlpatterns = [
    path("", views.simulation_list, name="simulation_list"),
    path("simulations/<int:pk>/", views.simulation_detail, name="simulation_detail"),
]