from django.db.models import Value, Case, When,F
from django.contrib.auth.models import BaseUserManager
from django.db.models.functions import Concat
from django.shortcuts import redirect


class CustomUserManager(BaseUserManager):
    
    def get_fullname(self):
        return self.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("Phone fields is required")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)
