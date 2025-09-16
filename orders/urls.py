from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.order_list, name="order_list"),
    path("create/", views.create_order, name="create_order"),
    path("<int:order_id>/edit/", views.edit_order, name="edit_order"),
    path("<int:order_id>/delete/", views.delete_order, name="delete_order"),
]
