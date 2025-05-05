from django.urls import path
from . import views

app_name = 'hod'  # Set the namespace for the app

urlpatterns = [
    path('head_dashboard/', views.head_dashboard, name='head_dashboard'),
    path('edit_profile_hod/', views.edit_profile_hod, name='edit_profile_hod'),
    path('head_dashboard/manage_project/', views.manage_project, name='manage_project'),
    # path('view_projects/<int:id>', views.view_projects, name='view_projects'),
    path('head_dashboard/manage_project/view_projects', views.view_projects, name='view_projects'),

]


