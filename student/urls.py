from django.urls import path
from . import views

app_name = 'student'  # Set the namespace for the app

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit_project/', views.submit_project, name='submit_project'),
    path('edit_profile_student/', views.edit_profile_student, name='edit_profile_student'),
    path('abstract_list_view/', views.abstract_list_view, name='abstract_list_view'),
    path('group_members/', views.group_members, name='group_members'),
    path('projects_students/', views.projects_students, name='projects_students'),

]

