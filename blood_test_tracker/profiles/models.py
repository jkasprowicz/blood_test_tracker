from django.db import models
from django.contrib.auth.models import User, Group, Permission

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='sem bio')
    avatar = models.ImageField(upload_to='profiles', default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.user.username}"