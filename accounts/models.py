from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .managers import UserManger

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)
EGYPT_COUNTRY_CODE = '+20'
US_COUNTRY_CODE = '+1'

COUNTRY_CODE_CHOICES = (
    (EGYPT_COUNTRY_CODE, 'EG'),
    (US_COUNTRY_CODE, 'US'),
)

# TWILO_REGEX = r'^\+[1-9]\d{10,14}$'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=False)
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    country_code = models.CharField(max_length=3, choices=COUNTRY_CODE_CHOICES, null=False,
                                    validators=[RegexValidator(regex=r'^\+\d{1,2}$',
                                                               message="Must be in E.164 i.e +xx")])
    phone = models.CharField(max_length=13, null=False,
                             validators=[RegexValidator(regex=r'^\d{10,14}$',
                                                        message="Must be in E.164 i.e xxxxxxxxxxx")])
    is_staff = models.BooleanField(_('staff status'), default=False)
    objects = UserManger()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['country_code', 'phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('country_code', 'phone',)

    def get_phone(self):
        return '%s%s' % (self.country_code, self.phone)

    def __str__(self):
        return self.get_full_name()

    def natural_key(self):
        return self.phone

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
