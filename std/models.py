from enum import Enum

from django.db import models
from datetime import date
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


# Create your models here.
class Role_Used(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class User(models.Model):
    userid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Active')
    role = models.ForeignKey(Role_Used, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        existing_email = User.objects.filter(email=self.email).exclude(pk=self.pk)
        if existing_email.exists():
            raise ValidationError("Email address already exists.")
