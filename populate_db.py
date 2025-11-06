import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment BEFORE importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
django.setup()

from task.models import CustomUser, Task, TaskDetail, Project

def populate():
    # Ensure projects exist before assigning them to tasks
    if not Project.objects.exists():
        print("No projects found! Please add at least one project before running this script.")
        return

    project = Project.objects.first()  # Assign tasks to the first project
    
    # Fetch all users to assign tasks
    users = list(CustomUser.objects.all())
    if not users:
        print("No users found! Please add users before running this script.")
        return
    
    # Task Titles & Descriptions
    task_titles = ["Fix Bug #123", "Implement Authentication", "Refactor API Endpoints", "Optimize Database Queries"]
    descriptions = ["Fixing a critical bug.", "Adding JWT authentication.", "Improving code structure.", "Enhancing query performance."]
    statuses = ["Pending", "In Progress", "Completed"]
    
    # Creating tasks
    tasks = []
    for i in range(10):  # Creating 10 tasks
        task = Task.objects.create(
            title=random.choice(task_titles),
            description=random.choice(descriptions),
            project=project,
            status=random.choice(statuses),
            due_date=datetime.now() + timedelta(days=random.randint(1, 30))
        )

        # ✅ Correct way to assign ManyToManyField
        assigned_users = random.sample(users, random.randint(1, min(3, len(users))))  # Assign 1-3 users
        task.assigned_to.set(assigned_users)  # Correct way

        tasks.append(task)
    
    # Creating task details
    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            additional_info=f"Details for {task.title}",
            created_at=datetime.now()
        )
    
    print("✅ Database population completed successfully!")

if __name__ == "__main__":
    populate()
