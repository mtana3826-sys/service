from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Необходимо указать телефон")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "owner")

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=20, unique=True)

    ROLE_CHOICES = [
        ("employee", "Сотрудник"),
        ("manager", "Управляющий"),
        ("owner", "Владелец"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="employee"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone