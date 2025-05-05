from django.db import models
from college_info.models import Department,Course

class Users(models.Model):
    
    user_role_choice = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    password = models.CharField(max_length=10,null=True,blank=True)
    contact_number = models.CharField(max_length=10,null=True,blank=True)
    message = models.CharField(max_length=300,null=True,blank=True)

    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to="static/images/profile_pictures/",  
        default="static/images/no_profile_pic.webp",  
        null=True, blank=True )


    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.name
    
class Student_Groups(models.Model):
    student_group_no = models.CharField(max_length=20,null=True,blank=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

