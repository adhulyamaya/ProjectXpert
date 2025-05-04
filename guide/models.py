from django.db import models
from user_management.models import Users

class TopicSubmission(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    submission_type = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.submission_type}"
