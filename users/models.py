import uuid

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = _('admin')
        MODERATOR = _('moderator')
        USER = _('user')

    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=False,
        validators=[validators.validate_email]
    )
    role = models.CharField(
        max_length=25,
        choices=Roles.choices,
        default=Roles.USER,
        null=False,
        blank=True
    )
    bio = models.TextField(blank=True)
    email_code = models.CharField(
        max_length=39,
        null=False,
        blank=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=100, blank=True,)
    last_name = models.CharField(max_length=100, blank=True,)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'
