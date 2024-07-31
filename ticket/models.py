
# Create your models here.
import uuid
from django.db import models
from users.models import User

class Ticket(models.Model):
    ticket_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    ticket_status = models.CharField(max_length=15, choices=[
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending')
    ])

    def __str__(self):
        return self.title
