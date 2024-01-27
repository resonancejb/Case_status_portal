from django.db import models
from django.contrib.auth.models import User 
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Case(models.Model):
    case_number = models.CharField(max_length=50)
    parties_involved = models.TextField()
    court_name = models.CharField(max_length=100) 
    previous_hearing = models.DateField(null=True, blank=True) 
    next_hearing = models.DateField(null=True, blank=True)
    hearing_date = models.DateField(null=True, blank=True)
    hearing_time = models.TimeField(null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases', null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  # Associate cases with users

    def __str__(self):
        return self.case_number
    # Can add more fields as needed

# new_case_created = django.dispatch.Signal()

@receiver(post_save, sender=Case)
def send_case_notification(sender, instance, created, **kwargs):
    if created:
        # Get the user associated with the case
        user = instance.client

        # Check if the user has a valid email
        if user.email:
            # Send notification here
            subject = 'New Case Scheduled'
            message = f'A new case with number {instance.case_number} has been scheduled for {instance.next_hearing}.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]  # Use the user's email as the recipient

            send_mail(subject, message, from_email, recipient_list)


