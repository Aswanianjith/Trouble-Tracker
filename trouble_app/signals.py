from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue, Comment
from django.core.mail import send_mail

@receiver(post_save, sender=Issue)
def issue_updated(sender, instance, created, **kwargs):
    if created:
        # Send email to the assigned user
        if instance.assigned_to:
            send_mail(
                'New Issue Assigned',
                f'You have been assigned a new issue: {instance.title}',
                'from@example.com',
                [instance.assigned_to.email],
                fail_silently=False,
            )
    else:
        # Send email to the assigned user about updates
        if instance.assigned_to:
            send_mail(
                'Issue Updated',
                f'The issue "{instance.title}" has been updated.',
                'from@example.com',
                [instance.assigned_to.email],
                fail_silently=False,
            )

@receiver(post_save, sender=Comment)
def comment_added(sender, instance, created, **kwargs):
    if created:
        # Send email to the issue creator and assigned user
        recipients = [instance.issue.created_by.email]
        if instance.issue.assigned_to and instance.issue.assigned_to.email not in recipients:
            recipients.append(instance.issue.assigned_to.email)
        send_mail(
            'New Comment on Issue',
            f'A new comment has been added to the issue: {instance.issue.title}',
            'from@example.com',
            recipients,
            fail_silently=False,
        )
