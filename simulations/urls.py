from django.urls import path
from . import views
from . import auth_views as authv

urlpatterns = [
    path("", views.simulation_list, name="simulation_list"),
    path("simulations/<int:pk>/", views.simulation_detail, name="simulation_detail"),
    path("simulations/new/", views.simulation_create, name="simulation_create"),  
    path("simulations/<int:pk>/edit/", views.simulation_update, name="simulation_update"),


    path("runs/new/", views.run_create, name="run_create"),
    path("simulations/<int:simulation_id>/runs/new/", views.run_create, name="run_create_for_sim"),
    path("runs/<int:pk>/edit/", views.run_update, name="run_update"),
    path("runs/<int:pk>/delete/", views.run_delete, name="run_delete"),

    path("accounts/register/", authv.register, name="register"),


]