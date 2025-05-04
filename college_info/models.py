from django.db import models

class College(models.Model):

    college_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.college_name
    

class Department(models.Model):

    department_name = models.CharField(max_length=100, null=True, blank=True)
    college_id = models.ForeignKey(College,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.department_name
    
class Course(models.Model):

    course_name = models.CharField(max_length=100, null=True, blank=True)
    batch = models.CharField(max_length=100, null=True, blank=True)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.course_name
    
