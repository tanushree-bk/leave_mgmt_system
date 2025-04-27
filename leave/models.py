#models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Type_leave(models.Model):
    name = models.CharField(max_length=200)
    no_days = models.PositiveIntegerField(default=0)

    def _str_(self):
        return self.name

class LeaveBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(Type_leave, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=timezone.now().year)
    balance = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'leave_type', 'year')

    def _str_(self):
        return f"{self.user.username} - {self.leave_type.name}"

class LeaveApplication(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(Type_leave, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def duration(self):
        return (self.end_date - self.start_date).days + 1

    def _str_(self):
        return f"{self.user.username} - {self.leave_type.name} ({self.status})"