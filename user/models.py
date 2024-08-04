from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        HOST = "HOST", "Host"
        PARTICIPANT = "PARTICIPANT", "Participant"
        
    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    
    # Assign the custom manager
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)

class Participant(User):
    base_role = User.Role.PARTICIPANT
    
    # Assign the custom manager
    objects = UserManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "Only for participant"

class Host(User):
    base_role = User.Role.HOST
    
    # Assign the custom manager
    objects = UserManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "Only for host"
