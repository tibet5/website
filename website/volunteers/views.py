from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, TemplateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from recipients.models import MealRequest, Delivery

from .tables import MealRequestTable
from .filters import MealRequestFilter
from .forms import DeliverySignupForm, ChefSignupForm, AcceptTermsForm
from .models import VolunteerApplication, VolunteerRoles


def delivery_success(request):
    return render(request, 'volunteers/delivery_success.html')


def chef_success(request):
    return render(request, 'volunteers/chef_success.html')


class IndexView(PermissionRequiredMixin, LoginRequiredMixin, SingleTableMixin, FilterView):
    model = MealRequest
    table_class = MealRequestTable
    filterset_class = MealRequestFilter
    template_name = "volunteers/index.html"
    permission_required = 'recipients.view_mealrequest'

    def anonymized_coordinates(self):
        instances = self.filterset.qs
        return {
            instance.id: [instance.anonymized_latitude, instance.anonymized_longitude, instance.id]
            for instance in instances
        }

    def google_maps_api_key(self):
        return settings.GOOGLE_MAPS_API_KEY


class DeliveryApplicationView(LoginRequiredMixin, FormView):
    form_class = AcceptTermsForm
    template_name = "volunteers/delivery_application.html"
    success_url = reverse_lazy('volunteers:delivery_application_received')

    def get(self, request, *args, **kwargs):
        has_applied = VolunteerApplication.objects.filter(
            user=self.request.user,
            role=VolunteerRoles.DELIVERERS,
        ).exists()
        if has_applied:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        VolunteerApplication.objects.create(
            user=self.request.user,
            role=VolunteerRoles.DELIVERERS,
        )
        return super().form_valid(form)


class DeliveryApplicationReceivedView(LoginRequiredMixin, TemplateView):
    template_name = "volunteers/delivery_application_received.html"


class DeliverySignupView(LoginRequiredMixin, FormView):
    model = Delivery
    template_name = "volunteers/delivery_signup.html"
    form_class = DeliverySignupForm
    success_url = reverse_lazy('volunteers:delivery_success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeliveryIndexView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = "volunteers/delivery_list.html"


class ChefApplicationView(LoginRequiredMixin, FormView):
    form_class = AcceptTermsForm
    template_name = "volunteers/chef_application.html"
    success_url = reverse_lazy('volunteers:chef_application_received')

    def get(self, request, *args, **kwargs):
        has_applied = VolunteerApplication.objects.filter(
            user=self.request.user,
            role=VolunteerRoles.CHEFS,
        ).exists()
        if has_applied:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        VolunteerApplication.objects.create(
            user=self.request.user,
            role=VolunteerRoles.CHEFS,
        )
        return super().form_valid(form)


class ChefApplicationReceivedView(LoginRequiredMixin, TemplateView):
    template_name = "volunteers/chef_application_received.html"


class ChefSignupView(LoginRequiredMixin, FormView):
    model = MealRequest
    template_name = "volunteers/chef_signup.html"
    form_class = ChefSignupForm
    success_url = reverse_lazy('volunteers:chef_success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChefIndexView(LoginRequiredMixin, ListView):
    model = MealRequest
    template_name = "volunteers/chef_list.html"
