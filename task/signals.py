from task.models import *
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Create a Signal(post_save):
# @receiver(post_save, sender=Task)
# def notify_task_creation(sender, instance, created, **kwargs):
    # if created:
        # instance.is_completed = True
        # instance.save()

# Create a Signal(pre_save):
@receiver(pre_save, sender=Task)
def notify_task_creation(sender, instance, **kwargs):
    instance.is_completed = True

@receiver(m2m_changed, sender=Task.assign_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_email = [] #all assigned email for a task
        for emp in instance.assign_to.all():
            assigned_email.append(emp.email)
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}.",
            "anisulalam2003@gmail.com",
            assigned_email,
        )

# @receiver(post_delete, sender=Task)
# def delete_associate_details(sender, instance, **kwargs):
    # if instance.details:
        # instance.details.delete()
