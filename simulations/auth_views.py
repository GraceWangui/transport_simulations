from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


"""
Handle user registration using Django's built-in UserCreationForm.

- If the request method is POST:
    - Instantiate the UserCreationForm with POST data.
    - Validate the form.
    - If valid, save the new user and log them in.
    - Redirect to the 'simulation_list' view upon successful registration.
- If the request method is not POST:
    - Instantiate an empty UserCreationForm for user input.

Renders the 'registration/register.html' template with the registration form.

Args:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered registration page or a redirect to 'simulation_list' after successful registration.
"""



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("simulation_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
