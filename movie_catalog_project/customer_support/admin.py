from typing import Any
from django.contrib import admin, messages
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.utils.translation import ngettext, gettext as _
from django.db.models import QuerySet
from . import models, utils


class TicketMessageInline(admin.TabularInline):
    model = models.TicketMessage
    extra = 0
    fields = ['body', 'sender_name', 'recipient_name', 'sent_at']
    readonly_fields = ['sender_name', 'recipient_name', 'sent_at']


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender_name', 'sent_at', 'status']
    list_display_links = ['subject', 'sender_name']
    list_filter = ['status', 'mail_sent', 'subject', 'sent_at']
    readonly_fields = ['mail_sent', 'sent_at', 'sender_email', 'sender_name', 'mail_sent', 'access_key']
    fields = ['subject', 'body', 'sender_name', 'sender_email', 'sender', 'status', 'sent_at', 'mail_sent', 'access_key']
    actions = ['mark_unread', 'mark_read', 'set_processing', 'close']
    inlines = [TicketMessageInline]

    def save_formset(self, request:HttpRequest, form: Any, formset: Any, change: Any) -> None:
        instances:list[models.TicketMessage] = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance._state.adding:
                instance.sender = request.user
                if instance.ticket.sender:
                    instance.recipient = instance.ticket.sender
                else:
                    instance.recipient_name = instance.ticket.sender_name
                    instance.recipient_email = instance.ticket.sender_email
                instance.clean()
                instance.save()
                utils.send_support_ticket_email(request, instance)
        formset.save_m2m()

    def change_view(
            self, 
            request: HttpRequest, 
            object_id: str, 
            form_url: str = "", 
            extra_context: dict[str, bool] | None = {}
        ) -> HttpResponse:
        obj = models.Ticket.objects.get(id=object_id)
        if obj.status == 'new':
            obj.status = 'read'
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description=_("mark unread").capitalize())
    def mark_unread(self, request:HttpRequest, queryset:QuerySet) -> None:
        updated = queryset.update(status='new')
        self.message_user(request, ngettext(
            "%d ticket has been made as new",
            "%d tickets have been made as new",
            updated
        ) % updated, messages.SUCCESS)

    @admin.action(description=_("mark read").capitalize())
    def mark_read(self, request:HttpRequest, queryset:QuerySet) -> None:
        updated = queryset.update(status='read')
        self.message_user(request, ngettext(
            "%d ticket has been marked as read",
            "%d tickets have been marked as read",
            updated
        ) % updated, messages.SUCCESS)    

    @admin.action(description=_("set processing").capitalize())
    def set_processing(self, request:HttpRequest, queryset:QuerySet) -> None:
        updated = queryset.update(status='processing')
        self.message_user(request, ngettext(
            "%d ticket has been set processing",
            "%d tickets have been set processing",
            updated
        ) % updated, messages.SUCCESS)

    @admin.action(description=_("close").capitalize())
    def close(self, request:HttpRequest, queryset:QuerySet) -> None:
        updated = queryset.update(status='closed')
        self.message_user(request, ngettext(
            "%d ticket has been closed",
            "%d tickets have been closed",
            updated
        ) % updated, messages.SUCCESS)

@admin.register(models.TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    pass
