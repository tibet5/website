import functools
import logging
import re
import urllib.parse
from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from website.maps import Geocoder, GeocoderException

logger = logging.getLogger(__name__)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def has_group(user, group_name: str):
    """Test whether the user is in a group with the given name"""
    return user.groups.filter(name=group_name).exists()


def group_names(user):
    """Returns a list of group names for the user"""
    return list(user.groups.all().values_list('name', flat=True))


class TelephoneInput(forms.TextInput):
    input_type = 'tel'

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs
        super().__init__(attrs={
            'pattern': r'\(?[0-9]{3}\)?[- ]?[0-9]{3}[- ]?[0-9]{4}',
            'title': 'Telephone input in the form xxx-xxx-xxxx',
            **attrs,
        })


class TelephoneFormField(forms.CharField):
    widget = TelephoneInput

    def clean(self, value):
        # Strip any extra characters from the phone number like ), (, space, or -
        return re.sub(r'[^0-9]', '', super().clean(value))


class TelephoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', 'Use the format 555-555-5555')
        kwargs.setdefault('max_length', settings.PHONE_NUMBER_LENGTH)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': TelephoneFormField,
            **kwargs,
        })


class Cities(models.TextChoices):
    EAST_YORK = 'East York', 'East York'
    ETOBICOKE = 'Etobicoke', 'Etobicoke'
    NORTH_YORK = 'North York', 'North York'
    SCARBOROUGH = 'Scarborough', 'Scarborough'
    TORONTO = 'Toronto', 'Toronto'
    YORK = 'York', 'York'


class ContactMixin(models.Model):
    class Meta:
        abstract = True

    name = models.CharField("Full name", max_length=settings.NAME_LENGTH)
    phone_number = TelephoneField("Phone number")
    email = models.EmailField("Email address")


class DemographicMixin(models.Model):
    class Meta:
        abstract = True

    bipoc = models.BooleanField("Black, Indigenous, and People of Colour (BIPOC)")
    lgbtq = models.BooleanField("Lesbian, Gay, Bisexual, Trans, Queer (LGBTQ), gender non-conforming or non-binary")
    has_disability = models.BooleanField("Living with disabilities")
    immigrant_or_refugee = models.BooleanField("Newly arrived immigrant or refugee")
    housing_issues = models.BooleanField("Precariously housed (no fixed address, living in a shelter, etc.)")
    sex_worker = models.BooleanField("Sex worker")
    single_parent = models.BooleanField("Single parent")
    senior = models.BooleanField("Senior citizen")


class TimestampsMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AddressMixin(models.Model):
    class Meta:
        abstract = True

    address_1 = models.CharField(
        "Address line 1",
        help_text="Street name and number",
        max_length=settings.ADDRESS_LENGTH
    )
    address_2 = models.CharField(
        "Address line 2",
        help_text="Apartment, Unit, or Suite number",
        max_length=settings.ADDRESS_LENGTH,
        blank=True,
    )
    city = models.CharField(
        "City",
        max_length=settings.CITY_LENGTH,
        choices=Cities.choices,
        default=Cities.TORONTO,
    )
    postal_code = models.CharField(
        "Postal code",
        max_length=settings.POSTAL_CODE_LENGTH
    )
    anonymized_latitude = models.FloatField(default=43.651070, blank=True)  # default: Toronto latitude
    anonymized_longitude = models.FloatField(default=-79.347015, blank=True)  # default: Toronto longitude

    @property
    def province(self):
        return "Ontario"

    @property
    def address(self):
        return f"{self.address_1} {self.address_2} {self.city} {self.province} {self.postal_code}"

    @property
    def address_link(self):
        address = urllib.parse.quote(self.address)
        return f"https://www.google.com/maps/place/{address}"

    @property
    def anonymous_address_link(self):
        return f"https://www.google.com/maps/place/{self.anonymized_latitude},{self.anonymized_longitude}"

    @property
    def anonymous_map_embed(self):
        return f"https://www.google.com/maps/embed/v1/place?key={ settings.GOOGLE_MAPS_PRODUCTION_KEY }&q={self.anonymized_latitude},{self.anonymized_longitude}"

    @property
    def coordinates(self):
        return (self.anonymized_latitude, self.anonymized_longitude)

    @functools.cached_property
    def fetched_coordinates(self):
        return Geocoder().geocode_anonymized(self.address)

    def update_coordinates(self):
        """Updates, but does not commit, anonymized coordinates on the instance"""
        try:
            latitude, longitude = self.fetched_coordinates
            self.anonymized_latitude = latitude
            self.anonymized_longitude = longitude
        except GeocoderException:
            logger.exception("Error when updating coordinates for %d", self.id)

    def save(self, *args, **kwargs):
        # Whenever the model is updated, make sure coordinates are updated too
        self.update_coordinates()
        super().save(*args, **kwargs)
