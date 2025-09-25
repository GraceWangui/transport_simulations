from django.shortcuts import render, get_object_or_404
from .models import Simulation
# Create your views here.

def simulation_list(request):
    sims = Simulation.objects.all()
    return render(request, "simulations/simulation_list.html", {"sims": sims})

def simulation_detail(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)
    runs = sim.runs.all()
    return render(request, "simulations/simulation_detail.html", {"sim": sim, "runs": runs})
