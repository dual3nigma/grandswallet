from django.db import models
from django.utils.timezone import now
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=150, unique=True, validators=[UnicodeUsernameValidator()]
    )

    password = models.CharField(
        max_length=255, default=''
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        abstract = True


class Address(models.Model):
    street = models.CharField(
        max_length=1024
    )

    outdoor_number = models.CharField(
        max_length=12
    )

    interior_number = models.CharField(
        max_length=12, default=''
    )

    neighborhood = models.CharField(
        max_length=64
    )

    municipality = models.CharField(
        max_length=64
    )

    city = models.CharField(
        max_length=64
    )

    state = models.CharField(
        max_length=64
    )

    country = models.CharField(
        max_length=64
    )

    postal_code = models.CharField(
        max_length=5
    )

    created_date = models.DateTimeField(
        default=now
    )

    class Meta:
        abstract = True


class Phone(models.Model):
    phone_number = models.CharField(
        max_length=10
    )

    created_date = models.DateTimeField(
        default=now
    )

    class Meta:
        abstract = True


class Email(models.Model):
    email_address = models.EmailField(
    )

    created_date = models.DateTimeField(
        default=now
    )

    class Meta:
        abstract = True


class Document(models.Model):

    # TODO: Add type of document (ej.. passport, id)

    document_file = models.FileField(
        upload_to='customers/documents'
    )

    created_date = models.DateTimeField(
        default=now
    )

    class Meta:
        abstract = True


class Account(models.Model):
    name = models.CharField(
        max_length=255
    )

    # TODO: Add type of the account (ej.: N2, N4, etc.)

    clabe = models.CharField(
        max_length=18
    )

    reference = models.CharField(
        max_length=255
    )

    contract = models.CharField(
        max_length=255
    )

    created_date = models.DateTimeField(
        default=now
    )

    class Meta:
        abstract = True