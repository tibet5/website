from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView

from core.models import group_names
from .forms import UserCreationForm, VolunteerProfileForm
from volunteers.models import Volunteer


class UserCreationView(FormView):
    form_class = UserCreationForm
    template_name = "core/signup.html"
    success_url = reverse_lazy('public:index')

    def form_valid(self, form):
        # Save the form to create the user
        # Then call login to make sure they're logged in before redirecting
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Volunteer
    form_class = VolunteerProfileForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return Volunteer.objects.get(user=self.request.user)

    def get_pending_group_names(self, user):
        return list(user.volunteer_applications.filter(
            approved=False,
        ).values_list('role', flat=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = group_names(self.request.user)
        context["pending_groups"] = self.get_pending_group_names(self.request.user)
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile details updated')
        return super().form_valid(form)
