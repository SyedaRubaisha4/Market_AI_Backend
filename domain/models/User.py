from django.db import models

from .BaseModel import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=(('Active', 'Active'), ('Suspended', 'Suspended')),
        default='Active',
    )

    class Meta:
        db_table = 'users'
