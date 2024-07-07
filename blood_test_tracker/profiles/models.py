from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class UserProfile(models.Model):
    USER_ROLES = [
        ('medico', 'Médico'),
        ('nutricionista', 'Nutricionista'),
        ('pacient', 'Paciente'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)

    def __str__(self):
        return self.user.username
