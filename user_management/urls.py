from django.urls import path
from . import views

app_name = 'user_management'  # Set the namespace for the app

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL for login page
    path('logout/', views.logout_view, name='logout'),  # URL for login page
    path('register/', views.register, name='register'),  # URL for register page
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('services/', views.services, name='services'), 
    path('contact_us/', views.contact_us, name='contact_us'),
    path('send_message/<int:id>/', views.message, name='send_message'),
    path('inbox', views.inbox, name='inbox'),

]
