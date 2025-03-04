from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    # Adding custom related_name to avoid reverse accessor conflict
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change related_name to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change related_name to avoid conflict
        blank=True,
    )

    def __str__(self):
        return self.username
    
# create and instructor 
class Instructor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # You can add other fields as needed
    def __str__(self):
        return f'{self.user.username} - Instructor'
