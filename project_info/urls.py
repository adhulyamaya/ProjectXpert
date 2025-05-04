from django.urls import path
from . import views

app_name = 'project_info'  # Set the namespace for the app

urlpatterns = [
    path('course/<int:course_id>/students/', views.course_students_view, name='course_students'),
    path('project_details', views.project_details, name='project_details'),

]