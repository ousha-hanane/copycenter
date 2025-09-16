from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, OrderFileForm
from .models import Order  
from django.shortcuts import get_object_or_404


@login_required
def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        file_form = OrderFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            uploaded_file = file_form.save(commit=False)
            uploaded_file.order = order
            uploaded_file.save()
            return redirect("order_list")
    else:
        form = OrderForm()
        file_form = OrderFileForm()
    return render(request, "orders/create_order.html", {"form": form, "file_form": file_form})



@login_required
def order_list(request):
    # On filtre les commandes créées par l'utilisateur connecté
    orders = Order.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})



@login_required
@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, created_by=request.user)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        file_form = OrderFileForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            # Vérifier si un nouveau fichier a été envoyé
            uploaded_file = request.FILES.get("file")
            if uploaded_file:
                # Supprimer les anciens fichiers liés
                for old in order.files.all():
                    if old.file:
                        old.file.delete(save=False)  # supprime le fichier physique
                    old.delete()

                # Sauvegarder le nouveau fichier
                if file_form.is_valid():
                    new_file = file_form.save(commit=False)
                    new_file.order = order
                    new_file.save()

            return redirect("order_list")
    else:
        form = OrderForm(instance=order)
        file_form = OrderFileForm()

    return render(request, "orders/edit_order.html", {
        "form": form,
        "file_form": file_form,
        "order": order,
    })


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, created_by=request.user)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")
    return render(request, "orders/delete_order.html", {"order": order})
