from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        # Si l’utilisateur est connecté, on l’envoie directement vers ses commandes
        return redirect("order_list")
    return render(request, "core/home.html")
