from django.urls import path
from . import views

app_name = 'guide'  # Set the namespace for the app

urlpatterns = [
    path('guide_dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('edit_profile_guide/', views.edit_profile_guide, name='edit_profile_guide'),
    path('submit_topic/', views.submit_topic, name='submit_topic'),
    path('project_ranking/', views.project_ranking, name='project_ranking'),
    path('handle_project_action/<int:project_id>/', views.handle_project_action, name='handle_project_action'),
    
]