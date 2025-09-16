from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from core.models import Department
from pypdf import PdfReader


class Order(models.Model):
    TYPE_CHOICES = [
        ("IMPRESSION", "Impression"),
        ("PHOTOCOPIE", "Photocopie"),
    ]
    STATUS_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("SOUMISE", "Soumise"),
        ("VALIDÉE", "Validée"),
        ("REFUSÉE", "Refusée"),
        ("EN_COURS", "En cours"),
        ("TERMINÉE", "Terminée"),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    copies = models.PositiveIntegerField(default=1)
    pages = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="BROUILLON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} - {self.title}"


class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="orders/", validators=[FileExtensionValidator(["pdf"])])
    page_count = models.PositiveIntegerField(default=0)
    original_filename = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # Compter les pages si c'est un PDF
        if self.file and self.file.name.lower().endswith(".pdf"):
            try:
                self.file.seek(0)
                reader = PdfReader(self.file)
                self.page_count = len(reader.pages)
            except Exception:
                self.page_count = 0
        if not self.original_filename and self.file:
            self.original_filename = self.file.name

        super().save(*args, **kwargs)

        # Recalculer le total de pages sur la commande
        order = self.order
        total_pages = sum(f.page_count for f in order.files.all())
        order.pages = total_pages
        order.save(update_fields=["pages"])
