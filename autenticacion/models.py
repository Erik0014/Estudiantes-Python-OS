from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]
    rol = models.CharField(
        max_length=20, choices=ROL_CHOICES, default='estudiante')
    telefono = models.CharField(max_length=15, blank=True)

    def _str_(self):
        return f"{self.get_full_name()} ({self.rol})"
