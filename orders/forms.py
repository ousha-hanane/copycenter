from django import forms
from .models import Order, OrderFile

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["department", "type", "title", "description", "copies"]  # ✅ champs visibles
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class OrderFileForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ["file"]
