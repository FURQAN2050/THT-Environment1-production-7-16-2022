from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime

from . import models
from .models import User, Teacher
 

def ipn_receiver(sender, **kwargs):
    ipn_obj = sender
 
    if ipn_obj.payment_status == ST_PP_COMPLETED:
 
        # get user id and extend the subscription
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        subscription = models.Subscriptions.objects.get(name=ipn_obj.item_name)
        user.teacher.subscriptionType = subscription
        user.teacher.extendSubscription(subscription.getEndDate(datetime.date.today()))

        user.teacher.save()

        user.teacher.processingSubscription = False
 
        # Send a thank you email

        mail_subject = "Thank you for your payment"

        messagehtml = render_to_string('subscription_payment_email.html', {
                'user': user,
                'subscription': subscription.name,
                'end_date': user.teacher.goodUntil.strftime("%m/%d/%Y"),
            })

        messageplain = render_to_string('subscription_payment_email_plain.html', {
                'user': user,
                'subscription': subscription.name,
                'end_date': user.teacher.goodUntil.strftime("%m/%d/%Y"),
            })

        to_email = user.email

        email = EmailMultiAlternatives(
            mail_subject, messageplain, to=[to_email]
        )
        email.attach_alternative(messagehtml, "text/html")

        email.send()

    # check for failed subscription payment IPN
    # elif ipn_obj.txn_type == "subscr_failed":
    #     pass
 
    # # check for subscription cancellation IPN
    # elif ipn_obj.txn_type == "subscr_cancel":
    #     pass


valid_ipn_received.connect(ipn_receiver)