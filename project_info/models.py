from django.db import models
from user_management.models import Users,Student_Groups

class Abstract(models.Model):
    project_type = models.CharField(max_length=50, null=True, blank=True)
    abstract_title = models.CharField(max_length=100, null=True, blank=True)
    abstract_file_name = models.CharField(max_length=100, null=True, blank=True)
    guide_message = models.CharField(max_length=500, null=True, blank=True)
    hod_messageto_guide = models.CharField(max_length=500, null=True, blank=True)
    guide_messageto_hod = models.CharField(max_length=500, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    abstract_status = models.CharField(max_length=16, null=True, blank=True, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    group_id = models.ForeignKey(Student_Groups, on_delete=models.CASCADE)

    originality = models.IntegerField(null=True, blank=True)
    clarity = models.IntegerField(null=True, blank=True)
    feasibility = models.IntegerField(null=True, blank=True)
    relevance = models.IntegerField(null=True, blank=True)
    methodology = models.IntegerField(null=True, blank=True)
    presentation = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)
    justification = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.abstract_title or "Untitled Abstract"


class Project_Reviews(models.Model):

    review_date = models.DateField(null=True, blank=True)
    feedback = models.CharField(max_length=100,null=True, blank=True)
    project_status = models.CharField(max_length=16,null=True,blank=True, default='NOT_SUBMITTED')
    review_choices = models.CharField(max_length=10,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    group_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    abstract_id = models.ForeignKey(Abstract,on_delete=models.CASCADE)

    def __str__(self):
        return self.review_date

