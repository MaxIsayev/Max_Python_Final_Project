from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import get_template
from . import models

def send_support_ticket_email(request: HttpRequest, obj:models.Ticket | models.TicketMessage):
    if isinstance(obj, models.Ticket):
        template_text = get_template('customer_support/ticket_email_text.html')
        subject = obj.subject
        obj_id = obj.id
        recipient_email = settings.ADMIN_EMAIL
    elif isinstance(obj, models.TicketMessage):
        template_text = get_template('customer_support/ticketmessage_email_text.html')
        subject = obj.ticket.subject
        obj_id = obj.ticket.id
        recipient_email = obj.recipient_email
    else:
        raise TypeError("support ticket/message object type error")
    message = template_text.render({'obj': obj})
    try:
        send_mail(f"Support Ticket #{obj_id}: {subject}", message, obj.sender_email, [recipient_email], fail_silently=False)
    except Exception as error:
        messages.warning(request, _("Thank you. We had some issues ({}) but we still got your message.").format(error))
    else:
        obj.mail_sent = True
        obj.save()
        messages.success(request, _("Message sent. Thank you. We will get back to you as soon as we can."))
