import uuid
from django.db import models
from django.conf import settings
from .validators import validate_photo

def upload_photo(instance, filename):
    return f"requests/{uuid.uuid4()}.{filename.split('.')[-1].lower()}"

class RepairRequest(models.Model):
    URGENCY_CHOICES = [
        ("low", "Низкая"),
        ("medium", "Средняя"),
        ("high", "Высокая"),
    ]

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Готово"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="repair_requests"
    )
    branch = models.ForeignKey(
        "accounts.Branch",
        on_delete=models.CASCADE,
        related_name="repair_requests"
    )
    description = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    photo = models.ImageField(upload_to=upload_photo, validators=[validate_photo])
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка №{self.pk}"