import collections
import math
from django.contrib import admin, messages
from django import forms
from django.utils.html import format_html, format_html_join
from core.admin import user_link

from .models import (
    MealRequest,
    MealRequestComment,
    SendNotificationException,
    GroceryRequest,
    GroceryRequestComment,
)
from django.utils.translation import ngettext


def short_time(time_obj):
    try:
        return time_obj.strftime('%-I %p')
    except ValueError:
        return time_obj.strftime('%I %p')
    except AttributeError:
        return 'None'


class NotSelectedFilter(admin.SimpleListFilter):
    title = 'Not Selected'
    parameter_name = 'not_selected'

    def lookups(self, request, model_admin):
        return (
            ('Hide "Not Selected"', 'Hide "Not Selected"'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Hide "Not Selected"':
            queryset = queryset.exclude(status__in=(
                MealRequest.Status.NOT_SELECTED,
                GroceryRequest.Status.NOT_SELECTED,
            ))
        return queryset


class CompletedFilter(admin.SimpleListFilter):
    title = 'Completed'
    parameter_name = 'completed'

    def lookups(self, request, model_admin):
        return (
            ('Hide Completed', 'Hide Completed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Hide Completed':
            queryset = queryset.exclude(status__in=(
                *MealRequest.COMPLETED_STATUSES,
                *GroceryRequest.COMPLETED_STATUSES,
            ))
        return queryset


# Assign the current user as author when saving comments from a model admin
class CommentInlineFormSet(forms.models.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = super(CommentInlineFormSet, self).save_new(form, commit=False)
        obj.author = self.request.user
        if commit:
            obj.save()
        return obj


# Abstract for all comment inlines
class CommentInline(admin.TabularInline):
    extra = 0
    ordering = (
        'created_at',
    )
    formset = CommentInlineFormSet
    readonly_fields = (
        'author',
    )

    # Add request to the formset so that we can access the logged-in user
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class MealRequestCommentInline(CommentInline):
    model = MealRequestComment


class MealRequestAdmin(admin.ModelAdmin):
    list_display = (
        'edit_link',
        'name',
        'phone_number',
        'texts',
        'city',
        'delivery_date',
        'pickup_range',
        'dropoff_range',
        'distance',
        'chef_link',
        'deliverer_link',
        'status',
        'completed',
        'created_at',
    )
    list_filter = (
        CompletedFilter,
        NotSelectedFilter,
        'status',
        'can_receive_texts',
        'created_at',
    )
    inlines = (
        MealRequestCommentInline,
    )
    actions = (
        'copy',
        'mark_as_confirmed',
        'mark_as_delivered',
        'notify_recipients_delivery',
        'notify_recipients_reminder',
        'notify_recipients_feedback',
        'notify_chefs_reminder',
        'notify_deliverers_reminder',
        'notify_deliverers_details',
    )
    search_fields = (
        '=id',
        'name',
        'email',
        'phone_number',
        'chef__volunteer__name',
        'deliverer__volunteer__name',
    )
    list_select_related = (
        'chef',
        'chef__volunteer',
        'deliverer',
        'deliverer__volunteer',
    )

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).with_delivery_distance()

    def texts(self, obj):
        return obj.can_receive_texts
    texts.boolean = True
    texts.short_description = "Texts"
    texts.admin_order_field = "can_receive_texts"

    def distance(self, obj):
        if obj.delivery_distance is None:
            return None

        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
            obj.directions_link,
            f"{math.ceil(obj.delivery_distance)} km",
        )

    def edit_link(self, request):
        return 'Edit request %d' % request.id
    edit_link.short_description = 'Edit link'

    def chef_link(self, obj):
        return user_link(obj.chef)
    chef_link.short_description = 'Chef'
    chef_link.admin_order_field = 'chef__volunteer__name'

    def deliverer_link(self, obj):
        return user_link(obj.deliverer)
    deliverer_link.short_description = 'Deliverer'
    deliverer_link.admin_order_field = 'deliverer__volunteer__name'

    def pickup_range(self, obj):
        return short_time(obj.pickup_start) + ' - ' + short_time(obj.pickup_end)
    pickup_range.short_description = 'Pickup range'

    def dropoff_range(self, obj):
        return short_time(obj.dropoff_start) + ' - ' + short_time(obj.dropoff_end)
    dropoff_range.short_description = 'Dropoff range'

    def completed(self, obj):
        return obj.status in MealRequest.COMPLETED_STATUSES
    completed.admin_order_field = 'status'
    completed.boolean = True

    def copy(self, request, queryset):
        for meal_request in queryset:
            new_meal_request = meal_request.copy()
            self.message_user(
                request,
                f"A copy of meal request {meal_request.id} has been created with new id {new_meal_request.id}",
                messages.SUCCESS,
            )
    copy.short_description = "Create a copy of selected meal request"

    def mark_as_confirmed(self, request, queryset):
        queryset = queryset.exclude(status=MealRequest.Status.DATE_CONFIRMED)
        updated = queryset.update(status=MealRequest.Status.DATE_CONFIRMED)

        if updated:
            self.message_user(request, ngettext(
                "%d meal request has been marked confirmed with recipient",
                "%d meal requests have been marked confirmed with recipient",
                updated,
            ) % updated, messages.SUCCESS)
        else:
            self.message_user(request, "No updates were made", messages.WARNING)
    mark_as_confirmed.short_description = "Mark as confirmed with the recipient"

    def mark_as_delivered(self, request, queryset):
        queryset = queryset.exclude(status=MealRequest.Status.DELIVERED)
        updated = queryset.update(status=MealRequest.Status.DELIVERED)

        if updated:
            self.message_user(request, ngettext(
                "%d meal request has been marked as delivered",
                "%d meal requests have been marked as delivered",
                updated,
            ) % updated, messages.SUCCESS)
        else:
            self.message_user(request, "No updates were made", messages.WARNING)
    mark_as_delivered.short_description = "Mark as delivered"

    def send_notifications(self, request, queryset, method_name):
        """
        Helper utility for invoking notification sending methods

        This is more complex than usual because we need to account for situations where we send a subset of notifications.
        Some notifications might succeed while others fail.
        If they all succeed, we simply emit the success message with a "Success" status
        If they partially fail, we emit info on both the successes and an error breakdown, with a "Warning" status
        If they all fail, we emit the error breakdown with a "Error" status

        method_name is the name of the method to invoke on each delivery instance.
        """
        successes, errors = [], []

        # Try to notify all recipients, capture any error messages that are received
        for meal_request in queryset:
            try:
                send_notification_method = getattr(meal_request, method_name)
                send_notification_method()
                successes.append(meal_request)
            except SendNotificationException as e:
                errors.append(e.message)

        sent = len(successes)
        unsent = len(errors)
        total = sent + unsent

        prefix_message = ngettext(
            "%d meal request was selected",
            "%d meal requests were selected",
            total,
        ) % total
        success_message = ngettext(
            "%d text message was sent",
            "%d text messages were sent",
            sent,
        ) % sent

        # An unordered list of grouped errors, along with the count of how many times the error happened
        error_messages = format_html_join(
            "\n", "<p><strong>{} message(s) not sent because: {}</strong></p>",
            ((count, error_message) for (error_message, count) in collections.Counter(errors).items()),
        )

        if sent and unsent:
            self.message_user(request, format_html("<p>{}</p><p>{}</p>{}", prefix_message, success_message, error_messages), messages.WARNING)
        elif sent:
            self.message_user(request, format_html("<p>{}</p><p>{}</p>", prefix_message, success_message), messages.SUCCESS)
        elif unsent:
            self.message_user(request, format_html("<p>{}</p>{}", prefix_message, error_messages), messages.ERROR)

    def notify_recipients_delivery(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_delivery_notification')
    notify_recipients_delivery.short_description = "Send text to recipients about delivery window"

    def notify_recipients_reminder(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_reminder_notification')
    notify_recipients_reminder.short_description = "Send text to recipients reminding them about TODAY's request"

    def notify_recipients_feedback(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_feedback_request')
    notify_recipients_feedback.short_description = "Send text to recipients requesting their feedback through form"

    def notify_chefs_reminder(self, request, queryset):
        self.send_notifications(request, queryset, 'send_chef_reminder_notification')
    notify_chefs_reminder.short_description = "Send text to chefs reminding them about the request"

    def notify_deliverers_reminder(self, request, queryset):
        self.send_notifications(request, queryset, 'send_deliverer_reminder_notification')
    notify_deliverers_reminder.short_description = "Send text to deliverers reminding them about the request"

    def notify_deliverers_details(self, request, queryset):
        self.send_notifications(request, queryset, 'send_detailed_deliverer_notification')
    notify_deliverers_details.short_description = "Send text to deliverers with details about TODAY's request"


class GroceryRequestCommentInline(CommentInline):
    model = GroceryRequestComment


class GroceryRequestAdmin(admin.ModelAdmin):
    list_display = (
        'edit_link',
        'name',
        'phone_number',
        'texts',
        'city',
        'delivery_date',
        'status',
        'completed',
        'created_at',
    )
    list_filter = (
        CompletedFilter,
        NotSelectedFilter,
        'status',
        'can_receive_texts',
        'created_at',
    )
    inlines = (
        GroceryRequestCommentInline,
    )
    search_fields = (
        '=id',
        'name',
        'email',
        'phone_number'
    )
    actions = (
        'mark_complete',
        'copy',
        'notify_recipients_scheduled',
        'notify_recipients_allergies',
        'notify_recipients_reminder',
        'notify_recipients_rescheduled',
        'notify_recipients_confirm_received',
    )

    def edit_link(self, request):
        return 'Edit request G%d' % request.id
    edit_link.short_description = 'Edit link'

    def texts(self, obj):
        return obj.can_receive_texts
    texts.boolean = True
    texts.short_description = "Texts"
    texts.admin_order_field = "can_receive_texts"

    def completed(self, obj):
        return obj.status in GroceryRequest.COMPLETED_STATUSES
    completed.admin_order_field = 'status'
    completed.boolean = True

    def send_notifications(self, request, queryset, method_name):
        """
        Helper utility for invoking notification sending methods

        This is more complex than usual because we need to account for situations where we send a subset of notifications.
        Some notifications might succeed while others fail.
        If they all succeed, we simply emit the success message with a "Success" status
        If they partially fail, we emit info on both the successes and an error breakdown, with a "Warning" status
        If they all fail, we emit the error breakdown with a "Error" status

        method_name is the name of the method to invoke on each request instance.
        """
        successes, errors = [], []

        # Try to notify all recipients, capture any error messages that are received
        for grocery_request in queryset:
            try:
                send_notification_method = getattr(grocery_request, method_name)
                send_notification_method()
                successes.append(grocery_request)
            except SendNotificationException as e:
                errors.append(e.message)

        sent = len(successes)
        unsent = len(errors)
        total = sent + unsent

        prefix_message = ngettext(
            "%d request was selected",
            "%d requests were selected",
            total,
        ) % total
        success_message = ngettext(
            "%d text message was sent",
            "%d text messages were sent",
            sent,
        ) % sent

        # An unordered list of grouped errors, along with the count of how many times the error happened
        error_messages = format_html_join(
            "\n", "<p><strong>{} message(s) not sent because: {}</strong></p>",
            ((count, error_message) for (error_message, count) in collections.Counter(errors).items()),
        )

        if sent and unsent:
            self.message_user(request, format_html("<p>{}</p><p>{}</p>{}", prefix_message, success_message, error_messages), messages.WARNING)
        elif sent:
            self.message_user(request, format_html("<p>{}</p><p>{}</p>", prefix_message, success_message), messages.SUCCESS)
        elif unsent:
            self.message_user(request, format_html("<p>{}</p>{}", prefix_message, error_messages), messages.ERROR)

    def notify_recipients_scheduled(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_scheduled_notification')
    notify_recipients_scheduled.short_description = "Send text to recipients about scheduled date"

    def notify_recipients_allergies(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_allergy_notification')
    notify_recipients_allergies.short_description = "Send text to recipients with allergy explanation"

    def notify_recipients_reminder(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_reminder_notification')
    notify_recipients_reminder.short_description = "Send text to remind recipients of today's delivery"

    def notify_recipients_rescheduled(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_rescheduled_notification')
    notify_recipients_rescheduled.short_description = "Send text to recipients with rescheduled explanation"

    def notify_recipients_confirm_received(self, request, queryset):
        self.send_notifications(request, queryset, 'send_recipient_confirm_received_notification')
    notify_recipients_confirm_received.short_description = "Send text to recipients to confirm they received their delivery"

    def mark_complete(self, request, queryset):
        updated = queryset.update(status=GroceryRequest.Status.DELIVERED)
        self.message_user(request, ngettext(
            "%d grocery request has been marked complete",
            "%d grocery requests have been marked complete",
            updated,
        ) % updated, messages.SUCCESS)
    mark_complete.short_description = "Mark selected grocery requests as complete"

    def copy(self, request, queryset):
        for grocery_request in queryset:
            new_grocery_request = grocery_request.copy()
            self.message_user(
                request,
                f"A copy of grocery request {grocery_request.id} has been created with new id {new_grocery_request.id}",
                messages.SUCCESS,
            )
    copy.short_description = "Create a copy of selected grocery request"


admin.site.register(MealRequest, MealRequestAdmin)
admin.site.register(GroceryRequest, GroceryRequestAdmin)
