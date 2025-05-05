from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Users,Student_Groups  # Import the custom Users model if you're using one
from college_info.models import Department,Course
import json



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)

            if user.password == password:
                request.session['user_id'] = user.id 
                if user.user_role_choice == 'Admin':
                    return redirect('hod:head_dashboard') 
                elif user.user_role_choice == 'Student':
                    return redirect('student:student_dashboard') 
                elif user.user_role_choice == 'Teacher':
                    return redirect('guide:guide_dashboard') 
                else:
                    messages.error(request, "User role is invalid.")
                    return redirect('user_management:login')
            else:
                messages.error(request, "Invalid password.")
                return redirect('user_management:login')

        except Users.DoesNotExist:
            messages.error(request, "Invalid email.")
            return redirect('user_management:login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_number = request.POST.get('contact_number')
        user_role_choice = request.POST.get('user_role_choice')
        department_name = request.POST.get('department_id')
        course_name = request.POST.get('course_id')
        group_id = request.POST.get('student_group_id')
        print('group_id', group_id)
        try:

            if Users.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect('user_management:register')
            
            # Create the new user object
            department_instance = Department.objects.get(department_name=department_name)
            
    
            course_instance = Course.objects.get(course_name=course_name)       
            user = Users(
                name=name,
                email=email,
                password=password,
                contact_number=contact_number,
                user_role_choice=user_role_choice,
                department_id=department_instance,
                course_id=course_instance
            )           
            # Save the user to the database
            user.save()
                       
            
            # If the user is a student and group_id is provided, create Student_Groups entry
            if user_role_choice == 'Student':
                if group_id:
                    try:
                        print(f"Attempting to create Student_Groups entry for user {user.id} with group {group_id}")
                        
                        # Create the Student_Groups entry
                        group = Student_Groups.objects.create(
                            student_group_no=group_id,
                            user_id=user
                        )

                        print('Student_group:', group)
                        
                        print(f"Successfully created Student_Groups entry:")
                        print(f"Group ID: {group.id}")
                        print(f"Group Number: {group.student_group_no}")
                        print(f"User ID: {group.user_id.id}")
                        print(f"User Name: {group.user_id.name}")
                        
                    except Exception as e:
                        print(f"Error creating Student_Groups entry: {str(e)}")
                        print(f"Error type: {type(e).__name__}")
                        print(f"User details - ID: {user.id}, Name: {user.name}, Email: {user.email}")
                        print(f"Attempted group number: {group_id}")
                    
                    # You can choose to continue registration even if group creation fails
                    messages.warning(request, "User registered but group assignment failed. Please contact admin.")
                
            
            messages.success(request, "Registration successful! You can now login.")
            return redirect('user_management:login')

        except Department.DoesNotExist:
    
            messages.error(request, "Selected department does not exist.")
            return redirect('user_management:register')
            
        except Course.DoesNotExist:
            
            messages.error(request, "Selected course does not exist.")
            return redirect('user_management:register')
            
        except Exception as e:
            # Handle other exceptions
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('user_management:register')
            
    else:
        return render(request, 'register.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def services(request):
    return render(request, 'services.html')


def contact_us(request):
    return render(request, 'contact_us.html')

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Users
import json

def message(request, id):
    # Step 1: Retrieve the user by ID
    user = get_object_or_404(Users, id=id)

    # Step 2: Process the form data on POST request
    if request.method == "POST":
        topic = request.POST.get('topic')  # Get the topic from form data
        guide_message = request.POST.get('guide_message')  # Get the message from form data

        # Create the new message object (including topic and message)
        new_message = {
            'topic': topic,
            'message': guide_message,
        }

        # If there are old messages, append the new message
        if user.message:
            old_messages = json.loads(user.message)  # Assuming the field contains JSON data
        else:
            old_messages = []

        # Append the new message to the existing ones
        old_messages.append(new_message)

        # Step 3: Save the updated messages list as JSON
        user.message = json.dumps(old_messages)
        user.save()

        # Optional: Return a success response or redirect
        return JsonResponse({"status": "success", "message": "Message saved successfully!"})

    # Step 4: Render the message page with existing user info
    return render(request, 'send_message.html', {'user': user})



def logout_view(request):
    logout(request)
    return render(request, 'login.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Users
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages as django_messages
from .models import Users
import json

def inbox(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_management:login')

    user = get_object_or_404(Users, id=user_id)

    # Load messages or initialize empty list
    if user.message:
        messages_list = json.loads(user.message)
    else:
        messages_list = []

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "send":
            # Handle sending a new message
            topic = request.POST.get('topic')
            message_text = request.POST.get('message')

            new_message = {
                'topic': topic,
                'message': message_text,
                'reply': None
            }

            messages_list.append(new_message)
            user.message = json.dumps(messages_list)
            user.save()
            django_messages.success(request, "Message sent successfully!")
            return redirect('user_management:inbox')

        elif action == "reply":
            # Handle replying to a message
            reply_index = int(request.POST.get('reply_index'))
            reply_text = request.POST.get('reply_text')

            if 0 <= reply_index < len(messages_list):
                messages_list[reply_index]['reply'] = reply_text
                user.message = json.dumps(messages_list)
                user.save()
                django_messages.success(request, "Reply sent successfully!")
            else:
                django_messages.error(request, "Invalid message index.")
            return redirect('user_management:inbox')

    return render(request, 'inbox.html', {'user': user, 'messages': messages_list})

