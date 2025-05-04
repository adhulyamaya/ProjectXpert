from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from college_info.models import Department, Course, College
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from project_info.models import Abstract, Project_Reviews
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from user_management.models import Users,Student_Groups
import json

import smtplib
from email.mime.text import MIMEText
import os
from django.conf import settings



def student_dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'studentdashboard.html', {'error': 'User not logged in'})

    user = get_object_or_404(Users, id=user_id)

    # Related models
    course = user.course_id  # ForeignKey to Course
    department = user.department_id  # ForeignKey to Department
    college = department.college_id if department else None  # College via Department

    student_group = Student_Groups.objects.filter(user_id=user).first()  # Optional

    context = {
        'user': user,
        'course': course,
        'department': department,
        'college': college,
        'student_group': student_group
    }

    return render(request, 'studentdashboard.html', context)


def send_email(to_email, subject, body):
    sender_email = "tpccasm@gmail.com"
    sender_password = "eyoa ykng firb sdhq"  # Use environment variable for production
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# def submit_project(request):
#     if request.method == 'POST':
#         user_id = request.session.get('user_id')

#         if not user_id:
#             return render(request, 'studentdashboard.html', {'error': 'User not logged in'})

#         user = get_object_or_404(Users, id=user_id)
#         user_ins = Users.objects.get(id=user_id)
#         print(user_ins)
#         id = user_ins.id
#         print(id)
#         # Get Student_Groups instance for this user
#         student_group = Student_Groups.objects.get(user_id=id)

#         project_title = request.POST.get('project_title')
#         project_abstract = request.FILES.get('project_file')

#         try:
#             # Save file to a directory
#             abstract_filename = project_title
#             if project_abstract:
#                 upload_dir = os.path.join(settings.MEDIA_ROOT, 'abstracts')
#                 os.makedirs(upload_dir, exist_ok=True)
#                 abstract_filename = os.path.join(upload_dir, project_abstract.name)
#                 with open(abstract_filename, 'wb+') as destination:
#                     for chunk in project_abstract.chunks():
#                         destination.write(chunk)

#             # Save project in DB
#             print('Abstract')
#             print(project_title)
#             print(project_abstract)

#             project = Abstract.objects.create(
#                 group_id=student_group,
#                 abstract_title=project_title,
#                 abstract_file_name=project_abstract  # assuming you have a FileField in your model
#             )

#             guides = Users.objects.filter(
#                 course_id=user.course_id,
#                 user_role_choice='Guide'
#             )

#             print(guides)

#             # Send email to guide (assuming user has a 'guide_email' field)
#             if hasattr(user, 'guide_email') and guides.email:
#                 try:
#                     subject = f"New Abstract Submitted: {project_title}"
#                     body = f"{user.name} has submitted a new abstract titled '{project_title}'."
#                     status = send_email(user.guide_email, subject, body)
#                     print(f"Email status: {status}")
#                 except Exception as e:
#                     print(f"Failed to send email to guide: {str(e)}")
#                     # Optionally log or store the error


#             messages.success(request, 'Project submitted successfully!')
#             return redirect('student:student_dashboard')  # Redirect to a page that lists submitted abstracts

#         except Exception as e:
#             messages.error(request, f'Error submitting project: {str(e)}')

#     return render(request, 'abstract_list.html')


def abstract_list_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'studentdashboard.html', {'error': 'User not logged in'})

    # Get the Student_Groups instance for this user
    student_group = get_object_or_404(Student_Groups, user_id=user_id)
    print("st", student_group)

    # Get Abstracts for the group, ordered from latest to oldest
    abstract_list = Abstract.objects.filter(group_id=student_group).order_by('-created_at')

    for abstract in abstract_list:
        abstract.uploader_name = abstract.group_id.user_id.name
        print(abstract.abstract_file_name)

    print(abstract_list)

    context = {
        'abstract_list': abstract_list,
    }
    return render(request, 'abstract_list.html', context)






def edit_profile_student(request):
    try:
        # Get user ID from session
        user_id = request.session.get('user_id')
        if not user_id:
            print('User ID not found in session.')
            return redirect('user_management:login')

        # Retrieve user object from database
        user = get_object_or_404(Users, id=user_id)
        print(f'Editing profile for user: {user.id}, {user.name}')

        if request.method == 'POST':
            # Debug the received POST data
            print(f"POST data: {request.POST}")
            print(f"Files data: {request.FILES}")

            # Update user profile fields
            user.name = request.POST.get('name', user.name)
            user.email = request.POST.get('email', user.email)
            user.contact_number = request.POST.get('contact_number', user.contact_number)

            # Department via ID
            department_id = request.POST.get('department_id')
            if department_id:
                print(department_id)
                department_obj = Department.objects.filter(department_name=department_id).first()
                print(department_obj)
                if department_obj:
                    user.department_id = department_obj
                    print(f"Assigned department: {department_obj.department_name}")
                else:
                    print(f"Department with ID {department_id} not found.")

            # Course via ID
            course_id = request.POST.get('course_id')
            print('course_id', course_id)
            if course_id:
                course_obj = Course.objects.filter(course_name=course_id).first()
                if course_obj:
                    user.course_id = course_obj
                    print(f"Assigned course: {course_obj.course_name}")
                else:
                    print(f"Course with ID {course_id} not found.")

            # Profile Picture Upload
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                print(f"Profile picture updated: {user.profile_picture.name}")

            # Save the updated user
            try:
                user.full_clean()  # This will validate the user instance
                user.save()
                print(f"User profile updated successfully: {user.id}")
                return redirect('student:student_dashboard')  # Redirect to student dashboard after successful profile update
            except ValidationError as e:
                print(f"Validation error occurred: {e.messages}")
                return render(request, 'studentdashboard.html', {  # Show the student dashboard with error messages
                    'guide_details': get_user_details(user),
                    'departments': Department.objects.all(),
                    'courses': Course.objects.all(),
                    'errors': e.messages,
                })

        # GET request
        return render(request, 'studentdashboard.html', {  # Show the student dashboard with current user details
            'guide_details': get_user_details(user),
            'departments': Department.objects.all(),
            'courses': Course.objects.all()
        })

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return render(request, 'student/studentdashboard.html', {  # Return to student dashboard if an error occurs
            'error_message': 'An unexpected error occurred. Please try again later.'
        })


def get_user_details(user):
    return {
        'name': user.name,
        'email': user.email,
        'contact_number': user.contact_number,
        'course_id': user.course_id.id if user.course_id else '',
        'department_id': user.department_id.id if user.department_id else '',
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
    }




def group_members(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'studentdashboard.html', {'error': 'User not logged in'})

    user = get_object_or_404(Users, id=user_id)

    student_group = Student_Groups.objects.filter(user_id=user).first()

    group_members = []
    if student_group:
        group_members = student_group.members.all()  # Assuming 'members' is a related name

    context = {
        'student_group': student_group,
        'group_members': group_members
    }

    return render(request, 'studentdashboard.html', context)



def projects_students(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'studentdashboard.html', {'error': 'User not logged in'})
    user = get_object_or_404(Users, id=user_id)
    student_group = Student_Groups.objects.filter(user_id=user).first()
    if not student_group:
        return render(request, 'project_student.html', {
            'student_group': None,
            'group_members': [],
            'abstract': None,
            'project_reviews': []
        })
    group_users = Student_Groups.objects.filter(student_group_no=student_group.student_group_no)
    group_members = [group.user_id for group in group_users]
    abstract = Abstract.objects.filter(group_id=student_group).first()
    project_reviews = []
    if abstract:
        project_reviews = Project_Reviews.objects.filter(abstract_id=abstract)
    context = {
        'student_group': student_group,
        'group_members': group_members,
        'abstract': abstract,
        'project_reviews': project_reviews,
    }
    return render(request, 'project_student.html', context)

# ========================================================================================================

import json
import fitz
from groq import Groq
from operator import itemgetter
from django.core.files.storage import FileSystemStorage


import fitz
import re


file_path = "path/to/student_abstract.pdf"
api_key = "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"


def project_abstract_pdf(file_path: str) -> str: 
    """Extract full text from a project abstract PDF file."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

# --- Step 3: Evaluate abstract using Groq LLM ---

def evaluate_project_abstract(abstract_text: str, api_key: str) -> Abstract:
    """Evaluate a project abstract using Groq LLM and return structured scoring data."""
    
    client = Groq(api_key=api_key)
    
    # Prepare the prompt for evaluation
    prompt = f"""
You are a project evaluator. Evaluate the following student project abstract on these criteria (0–10 scale):

- Originality
- Problem Clarity
- Technical Feasibility
- Real-World Relevance
- Methodology
- Overall Presentation

Then calculate total_score (sum of the above) and provide a 1–2 sentence justification.

Respond ONLY in the following JSON format:

{{
  "originality": int,
  "clarity": int,
  "feasibility": int,
  "relevance": int,
  "methodology": int,
  "presentation": int,
  "total_score": int,
  "justification": "string"
}}

Abstract:
\"\"\"{abstract_text}\"\"\"
    """
    
    try:
        # Send request to Groq API
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that evaluates project abstracts and returns JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192",  # Change the model as needed
            response_format={"type": "json_object"},
            temperature=0.5
        )
        
        # Extract the raw response content
        content = completion.choices[0].message.content
        print("[DEBUG] Raw Groq response:", content)
        
        # Try to extract valid JSON from the response
        start = content.find('{')
        end = content.rfind('}') + 1
        json_part = content[start:end]  # Isolate the JSON portion
        
        data = json.loads(json_part)  # Parse the JSON
        
        # Return structured Abstract object with the extracted evaluation data
        return Abstract(
            originality=data["originality"],
            clarity=data["clarity"],
            feasibility=data["feasibility"],
            relevance=data["relevance"],
            methodology=data["methodology"],
            presentation=data["presentation"],
            total_score=data["total_score"],
            justification=data["justification"],
            abstract=abstract_text
        )

    except Exception as e:
        print(f"Error calling Groq API (abstract evaluation): {e}")
        return Abstract(
            originality=0,
            clarity=0,
            feasibility=0,
            relevance=0,
            methodology=0,
            presentation=0,
            total_score=0,
            justification="Evaluation failed.",
            abstract=abstract_text
        )

def submit_project(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        print(f"[DEBUG] user_id from session: {user_id}")

        if not user_id:
            print("[ERROR] User not logged in.")
            return render(request, 'studentdashboard.html', {'error': 'User not logged in'})

        user = get_object_or_404(Users, id=user_id)
        print(f"[DEBUG] User fetched: {user}")

        student_group = get_object_or_404(Student_Groups, user_id=user.id)
        print(f"[DEBUG] Student group fetched: {student_group}")

        project_title = request.POST.get('project_title')
        project_abstract = request.FILES.get('project_file')

        print(f"[DEBUG] Received project title: {project_title}")
        print(f"[DEBUG] Received project abstract file: {project_abstract.name if project_abstract else 'None'}")

        try:
            if not project_abstract:
                print("[ERROR] No abstract file uploaded.")
                messages.error(request, 'No abstract file uploaded.')
                return redirect('student:student_dashboard')
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'abstracts')
            os.makedirs(upload_dir, exist_ok=True)
            saved_file_path = os.path.join(upload_dir, project_abstract.name)

            print(f"[DEBUG] Saving uploaded file to: {saved_file_path}")
            with open(saved_file_path, 'wb+') as destination:
                for chunk in project_abstract.chunks():
                    destination.write(chunk)
            print("[DEBUG] File saved successfully.")
            # Step 1: Parse the abstract text
            print("[DEBUG] Parsing PDF...")
            parsed_text = project_abstract_pdf(saved_file_path)
            print(f"[DEBUG] Parsed text length: {len(parsed_text)}")
            print(parsed_text,".........................")

            # Step 2: Evaluate via Groq
            print("[DEBUG] Sending parsed text to Groq API for evaluation...")
            evaluation = evaluate_project_abstract(parsed_text, api_key=api_key)
            print(f"[DEBUG] Evaluation result: {evaluation}")
            
            # Step 3: Store everything in DB
            print("[DEBUG] Creating Abstract instance in DB...")
            print("[DEBUG] Extracted Evaluation Values:")
            print("Originality:", evaluation.get("originality"))
            print("Clarity:", evaluation.get("clarity"))
            print("Feasibility:", evaluation.get("feasibility"))
            print("Relevance:", evaluation.get("relevance"))
            print("Methodology:", evaluation.get("methodology"))
            print("Presentation:", evaluation.get("presentation"))
            print("Total Score:", evaluation.get("total_score"))
            print("Justification:", evaluation.get("justification"))
            
            project = Abstract.objects.create(
                group_id=student_group,
                abstract_title=project_title,
                abstract_file_name=project_abstract.name,
                originality=evaluation.get("originality"),
                clarity=evaluation.get("clarity"),
                feasibility=evaluation.get("feasibility"),
                relevance=evaluation.get("relevance"),
                methodology=evaluation.get("methodology"),
                presentation=evaluation.get("presentation"),
                total_score=evaluation.get("total_score"),
                justification=evaluation.get("justification"),
            )
            print("[DEBUG] Abstract saved successfully to DB.")

            messages.success(request, 'Project submitted and evaluated successfully!')
            return redirect('student:student_dashboard')

        except Exception as e:
            print(f"[EXCEPTION] Error during project submission: {e}")
            messages.error(request, f'Error submitting project: {str(e)}')

    return render(request, 'abstract_list.html')
