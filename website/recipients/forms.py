from textwrap import dedent
from django import forms
from .models import MealRequest, GroceryRequest, Days, TimePeriods, Vegetables, Fruits, Grains, Condiments


class TelephoneInput(forms.TextInput):
    input_type = 'tel'

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs
        super().__init__(attrs={
            'pattern': r'\(?[0-9]{3}\)?[- ]?[0-9]{3}[- ]?[0-9]{4}',
            'title': 'Telephone input in the form xxx-xxx-xxxx',
            **attrs,
        })


class HelpRequestForm(forms.ModelForm):
    # Field overrides
    available_days = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Days.choices,
    )
    available_time_periods = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=TimePeriods.choices,
    )
    accept_terms = forms.BooleanField(required=True)

    terms_of_service_text = dedent("""
        I acknowledge that The People's Pantry IS NOT RESPONSIBLE FOR ANY ISSUES I MAY HAVE WITH THE FOOD THAT HAS BEEN DELIVERED TO ME. This may include, but is not limited to, allergies, food outside of dietary preferences or restrictions, or digestive tract issues caused by consuming the food. I understand that The People's Pantry will not knowingly provide me with food to which I have an allergy, is outside of my dietary restrictions, or foods that are otherwise unsafe to eat, but is not liable for any issues that may occur.

        I acknowledge that The People's Pantry IS NOT RESPONSIBLE FOR THE PRESERVATION OR PREPARATION OF ANY FOOD ONCE IT HAS BEEN DELIVERED TO ME. It is my sole responsibility to ensure that food is stored and cooked safely and that pre-cooked meals are reheated to safe temperatures.

        I acknowledge that The People's Pantry IS NOT RESPONSIBLE FOR ANY ISSUES I MAY HAVE DURING THE DELIVERY PROCESS. I understand that The People's Pantry screens all volunteers and that volunteers are to adhere to the safe delivery guidelines of The People's Pantry, but The People's Pantry is not liable for any issues caused by the volunteer. This includes, but is not limited to, delayed delivery, inappropriate behaviour, damage to property, etc. I understand that if an issue pertaining to the delivery process arises, I may contact The People's Pantry to report the volunteer, but in the event that any illegal activity occurs, it is my responsibility to contact law enforcement.

        I acknowledge that I AM NOT TO CONTACT THE DELIVERY VOLUNTEER OUTSIDE OF THE CONTEXT OF THE DELIVERY. I am not to disclose their name, phone number, or any other personal information to others.

        I understand that IF I DO NOT CONFIRM READINESS TO ACCEPT A DELIVERY IN A TIMELY FASHION or ACT AGGRESSIVELY AGAINST A VOLUNTEER, MY DELIVERY WILL NOT BE SCHEDULED.
    """)

    class Meta:
        exclude = ['uuid', 'created_at', 'updated_at', 'anonymized_latitude', 'anonymized_longitude']

        widgets = {
            'phone_number': TelephoneInput(),
            'requester_phone_number': TelephoneInput(),
            'food_allergies': forms.Textarea(attrs={'rows': 3}),
            'food_preferences': forms.Textarea(attrs={'rows': 3}),
            'delivery_details': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MealRequestForm(HelpRequestForm):
    class Meta(HelpRequestForm.Meta):
        model = MealRequest


class GroceryRequestForm(HelpRequestForm):
    class Meta(HelpRequestForm.Meta):
        model = GroceryRequest

    vegetables = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Vegetables.choices,
    )
    fruits = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Fruits.choices,
    )
    grains = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Grains.choices,
    )
    condiments = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Condiments.choices,
    )
