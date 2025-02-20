from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from multiselectfield import MultiSelectField

from core.models import ContactMixin, AddressMixin, TimestampsMixin
from .emails import VolunteerApplicationConfirmationEmail, VolunteerApplicationApprovalEmail


class CookingTypes(models.TextChoices):
    COOKING = 'Cooking', 'Cooking'
    BAKING = 'Baking', 'Baking'


class FoodTypes(models.TextChoices):
    MEAT = 'Meat', 'Meat'
    VEGAN = 'Vegan', 'Vegan'
    VEGETARIAN = 'Vegetarian', 'Vegetarian'
    DAIRY_FREE = 'Dairy-free', 'Dairy-free'
    GLUTEN_FREE = 'Gluten-free', 'Gluten-free'
    LOW_CARB = 'Low carb', 'Low carb'
    HALAL = 'Halal', 'Halal'
    KOSHER = 'Kosher', 'Kosher'


class TransportationTypes(models.TextChoices):
    SUV = 'SUV or Truck', 'SUV or Truck'
    MED_CAR = 'Medium-sized car', 'Medium-sized car'
    SM_CAR = 'Small car', 'Small car'
    BIKE_SUMMER = 'Bike - Spring to Fall deliveries only', 'Bike - Spring to Fall deliveries only'
    BIKE_ALL = 'Bike - Can deliver in snow', 'Bike - Can deliver in snow'
    PEDESTRIAN = 'Pedestrian', 'Pedestrian'
    PUBLIC_TRANSIT = 'Public Transit', 'Public Transit'


class DaysOfWeek(models.TextChoices):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


# These choice values must match up with the name of the Groups
class VolunteerRoles(models.TextChoices):
    CHEFS = 'Chefs'
    DELIVERERS = 'Deliverers'
    ORGANIZERS = 'Organizers'


# Organizer volunteers fall into the following categories
class OrganizerTeams(models.TextChoices):
    REQUESTS = ('Requests', 'Requests')
    VOLUNTEER_INTAKE = ('Volunteer Intake', 'Central Volunteer Intake')
    CHEF_COORDINATORS = ('Chef Coordinators', 'Chefs Coordinators')
    DELIVERER_COORDINATORS = ('Deliverer Coordinators', 'Delivery Volunteers Coordinators')
    FINANCES = ('Finances', 'Grants and Finances')
    TECH = ('Tech', 'Tech')
    SOCIAL_MEDIA = ('Social Media', 'Social Media')
    OUTREACH = ('Outreach', 'Outreach')


class Volunteer(ContactMixin, AddressMixin, models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="volunteer"
    )
    short_name = models.CharField(
        "Short name",
        help_text="(Optional) A short version of your name that we will use for your privacy when contacting recipients",
        max_length=settings.DEFAULT_LENGTH,
        null=True,
        blank=True,
    )
    pronouns = models.CharField(
        "Pronouns",
        help_text="Please include all of your pronouns",
        max_length=settings.DEFAULT_LENGTH,
        null=True,
        blank=True
    )
    days_available = MultiSelectField(
        "Days available",
        help_text="What days of the week are you available to volunteer?",
        max_length=settings.DEFAULT_LENGTH,
        choices=DaysOfWeek.choices,
        min_choices=1,
        null=True
    )
    total_hours_available = models.CharField(
        "Total commitment",
        help_text="How many hours a week are your willing to volunteer?",
        max_length=settings.DEFAULT_LENGTH,
        null=True
    )
    recurring_time_available = models.CharField(
        "Recurring availability",
        help_text="Are there any times when you're consistently available? E.g. Mondays from 1-6pm, etc.",
        max_length=settings.DEFAULT_LENGTH,
        null=True
    )
    have_ppe = models.BooleanField(
        "PPE",
        help_text="Do you have access to personal protective equipment such as masks, gloves, etc?",
        default=False
    )
    notes = models.CharField(
        "Notes",
        help_text="Please include any relevant info the coordinator may need to know, such as upcoming holidays, changes in circumstances, etc",
        max_length=settings.DEFAULT_LENGTH,
        null=True,
        blank=True
    )

    # Fields for cooks only
    cooking_prefs = MultiSelectField(
        "Cooking type",
        help_text="What do you prefer to cook/bake? Check all that apply.",
        max_length=settings.DEFAULT_LENGTH,
        choices=CookingTypes.choices,
        min_choices=1,
        null=True,
        blank=True
    )
    food_types = MultiSelectField(
        "Food types",
        help_text="What kind of meals/baked goods are you able to prepare? Check all that apply.",
        max_length=settings.DEFAULT_LENGTH,
        choices=FoodTypes.choices,
        min_choices=1,
        null=True,
        blank=True
    )
    have_cleaning_supplies = models.BooleanField(
        "Cleaning supplies",
        help_text="Do you have cleaning supplies (soap, disinfectant, etc.) to clean your hands and kitchen?",
        null=True,
        blank=True
    )
    baking_volume = models.CharField(
        "Baking volume",
        help_text="For BAKERS: how many 'units' of baked goods can you bake each time? E.g. 48 cookies, 24 cinnamon buns, etc",
        max_length=settings.DEFAULT_LENGTH,
        null=True,
        blank=True
    )

    # Fields for delivery people only
    transportation_options = MultiSelectField(
        "Transportation options",
        help_text="What means of transportation do you have access to for deliveries? Check all that apply.",
        max_length=settings.DEFAULT_LENGTH,
        choices=TransportationTypes.choices,
        min_choices=1,
        blank=True,
        null=True
    )
    training_complete = models.BooleanField("Training Complete", default=False)

    # Fields for organizers only
    organizer_teams = MultiSelectField(
        "Organizer teams",
        help_text="Which teams would you be interested in joining?",
        max_length=settings.DEFAULT_LENGTH,
        choices=OrganizerTeams.choices,
        min_choices=1,
        blank=True,
    )

    @classmethod
    def group_for_role(cls, role):
        return Group.objects.get(name=role)

    @property
    def preferred_name(self):
        return self.short_name or self.name

    def remove_permissions(self):
        self.user.groups.clear()
        self.user.save()


class VolunteerApplication(TimestampsMixin, models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'role'], name='unique role per user application')
        ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer_applications'
    )
    role = models.CharField(
        max_length=50,
        choices=VolunteerRoles.choices,
    )
    organizer_teams = MultiSelectField(
        "Organizer teams",
        help_text="Which teams would you be interested in joining?",
        max_length=settings.DEFAULT_LENGTH,
        choices=OrganizerTeams.choices,
        min_choices=1,
        blank=True,
    )
    approved = models.BooleanField(default=False)

    @classmethod
    def has_applied(cls, user, role: str):
        return cls.objects.filter(user=user, role=role).exists()

    def approve(self):
        """Approves the application if it hasn't been already.
        Returns False if the application has already been approved, else True
        """
        if self.approved:
            return False
        group = Volunteer.group_for_role(self.role)
        self.user.groups.add(group)
        self.approved = True
        self.save()
        self.send_approved_email()
        return True

    def send_confirmation_email(self):
        return VolunteerApplicationConfirmationEmail().send(self.user.email, {"application": self})

    def send_approved_email(self):
        return VolunteerApplicationApprovalEmail().send(self.user.email, {"application": self})


# When user is created or saved, also save volunteer
@receiver(post_save, sender=User)
def save_volunteer(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'volunteer'):
        Volunteer.objects.create(user=instance)
    instance.volunteer.save()
