from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Récupérer le rôle choisi
            role = form.cleaned_data.get("role")

            # Ajouter l’utilisateur dans le groupe correspondant
            if role == "Professeur":
                group, created = Group.objects.get_or_create(name="Professeur")
                user.groups.add(group)
            elif role == "Administratif":
                group, created = Group.objects.get_or_create(name="Administratif")
                user.groups.add(group)

            login(request, user)
            return redirect("order_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
