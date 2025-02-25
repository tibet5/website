from django.utils.html import format_html
from django.urls import reverse


def user_link(user):
    if user:
        display_text = user.volunteer.name or user
        url = reverse('admin:volunteers_volunteer_change', args=(user.id,))
        return format_html('<a href="%s">%s</a>' % (url, display_text))
    return user
