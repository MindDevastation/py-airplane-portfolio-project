from datetime import timedelta
from time import timezone

from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from station.models import Order, Flight


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Order #{instance.id} Confirmation"
        html_message = render_to_string(
            'order_confirmation_email.html', {'order': instance}
        )
        plain_message = strip_tags(html_message)
        from_email = 'no-reply@yourdomain.com'
        to_email = instance.user.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


@receiver(post_save, sender=Flight)
def send_flight_status_update(sender, instance, **kwargs):
    if instance.status in ["delayed", "cancelled"]:
        users = instance.get_users()
        if users:
            print(f"Flight status updated to: {instance.status}")
            subject = f"Flight {instance.id} Status Update"
            html_message = render_to_string(
                "flight_status_update_email.html", {"flight": instance}
            )
            plain_message = strip_tags(html_message)
            from_email = "no-reply@yourdomain.com"

            for user in users:
                send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)


@shared_task
def send_flight_reminder(flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return

    users = flight.get_users()
    if not users:
        return

    time_until_departure = flight.departure_time - timezone.now()

    if timedelta(minutes=0) <= time_until_departure <= timedelta(hours=1):
        subject = f"Reminder: Your Flight {flight.id} is in 1 hour!"
        html_message = render_to_string("flight_reminder_email.html", {"flight": flight})
        plain_message = strip_tags(html_message)
        from_email = "no-reply@yourdomain.com"

        for user in users:
            send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

