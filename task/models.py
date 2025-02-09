from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Employee model(table)
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Task model(table)
STATUS_CHOICES = [
    ("PENDING", 'Pending'),
    ("IN_PROGRESS", 'In Progress'),
    ("COMPLETED", 'Completed')
]
class Task(models.Model):
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1
    )
    assign_to = models.ManyToManyField(
        Employee
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Task Details model
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    PRIORITY_OPTION = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    # assign_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTION, default=LOW)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Task details for --> {self.task.title}"

# Project model
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name 

'''
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
'''