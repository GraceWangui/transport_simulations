from django.shortcuts import render, get_object_or_404, redirect
from simulations.forms import SimulationForm, RunForm
from .models import Simulation, Run
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def simulation_list(request):
    sims = Simulation.objects.all()
    return render(request, "simulations/simulation_list.html", {"sims": sims})

@login_required
def simulation_detail(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)
    runs = sim.runs.all()
    return render(request, "simulations/simulation_detail.html", {"sim": sim, "runs": runs})

@login_required
def simulation_create(request):
    if request.method == "POST":
        form = SimulationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("simulation_list")
    else:
        form = SimulationForm()
    return render(request, "simulations/simulation_form.html", {"form": form, "action": "Create"})

@login_required
def run_create(request, simulation_id=None):
    if request.method == "POST":
        form = RunForm(request.POST)
        if form.is_valid():
            run = form.save()
            return redirect("simulation_detail", pk=run.simulation_id)
    else:
        initial = {}
        if simulation_id is not None:
            initial["simulation"] = get_object_or_404(Simulation, pk=simulation_id)
        form = RunForm(initial=initial)
    return render(request, "simulations/run_form.html", {"form": form, "action": "Create"})

@login_required
def simulation_update(request, pk):
    sim = get_object_or_404(Simulation, pk=pk)
    if request.method == "POST":
        form = SimulationForm(request.POST, instance=sim)
        if form.is_valid():
            form.save()
            return redirect("simulation_detail", pk=sim.pk)
    else:
        form = SimulationForm(instance=sim)
    return render(request, "simulations/simulation_form.html", {"form": form, "action": "Update"})

@login_required
def run_update(request, pk):
    run = get_object_or_404(Run, pk=pk)
    if request.method == "POST":
        form = RunForm(request.POST, instance=run)
        if form.is_valid():
            run = form.save()
            return redirect("simulation_detail", pk=run.simulation_id)
    else:
        form = RunForm(instance=run)
    return render(request, "simulations/run_form.html", {"form": form, "action": "Update"})

@login_required
def run_delete(request, pk):
    run = get_object_or_404(Run, pk=pk)
    if request.method == "POST":
        sim_id = run.simulation_id
        run.delete()
        return redirect("simulation_detail", pk=sim_id)
    return render(request, "simulations/run_confirm_delete.html", {"run": run})
