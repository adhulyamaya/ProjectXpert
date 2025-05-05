from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from user_management.models import Users, Student_Groups
from django.templatetags.static import static
from college_info.models import Course, College, Department
from user_management.models import Users, Student_Groups
from project_info.models import Abstract, Project_Reviews
import os

def head_dashboard(request):
    # Get user_id from session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_management:login')  # Redirect to login if not logged in

    # Get the logged-in user or return 404 if not found
    user = get_object_or_404(Users, id=user_id)

    profile_path = str(user.profile_picture)
    if profile_path.startswith("static/"):
        # Remove 'static/' and use the {% static %} tag to resolve correctly
        pro_pic = static(profile_path.replace("static/images", ""))
    else:
        pro_pic = user.profile_picture.url  # For normal media files

    student_groups = Student_Groups.objects.filter(user_id=user)
    department_name = user.department_id.department_name

    context = {
        'user': user,
        'pro_pic': pro_pic,
        'department_name': department_name,
        'student_groups': student_groups,
    }
    return render(request, 'head_dashboard.html', context)



def edit_profile_hod(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_management:login')

    # Fetch the HOD user
    user = get_object_or_404(Users, id=user_id)

    if request.method == 'POST':
        # Update basic fields
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        user.contact_number = request.POST.get('contact_number', user.contact_number)

        # Update course if provided
        course_name = request.POST.get('course')
        if course_name:
            course_obj = Course.objects.filter(course_name=course_name).first()
            if course_obj:
                user.course_id = course_obj

        # Update department if provided
        department_name = request.POST.get('department')
        if department_name:
            department_obj = Department.objects.filter(department_name=department_name).first()
            if department_obj:
                user.department_id = department_obj


        # Save safely
        try:
            user.full_clean()
            user.save()
            return redirect('hod:head_dashboard')  # <-- Redirect to HOD's dashboard after editing
        except ValidationError as e:
            # You can optionally pass validation errors back to template
            return render(request, 'edit_profile_hod.html', {
                'guide_details': get_user_details(user),
                'errors': e.messages,
            })

    # If GET request, render the form with current user details
    return render(request, 'edit_profile.html', {
        'guide_details': get_user_details(user)
    })

def get_user_details(user):
    """Helper function to extract user details nicely."""
    return {
        'name': user.name,
        'email': user.email,
        'contact_number': user.contact_number,
        'course': user.course_id.course_name if user.course_id else '',
        'department': user.department_id.department_name if user.department_id else '',
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
    }


def manage_project(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_management:login')

    user = get_object_or_404(Users, id=user_id)

    # Filter all users with role 'GUIDE' in the same department
    guide_users = Users.objects.filter(user_role_choice='Teacher', department_id=user.department_id)
    print(user)
    print(guide_users)
    context = {
        'user': user,
        'guide_users': guide_users
    }

    return render(request, 'manage_project.html', context)




# def view_projects(request, id):
#     user_id = request.session.get('user_id')
#     print('user_id', user_id)   
#     if not user_id:
#         return redirect('user_management:login')

#     user = get_object_or_404(Users, id=user_id)
    
#     guide = get_object_or_404(Users, id=id)  

#     department =

#     student_groups = Student_Groups.objects.filter(user_id=guide)
#     print('student_groups', student_groups)

#     data = []


#     for group in student_groups:
#         abstracts = Abstract.objects.filter(group_id=group)
#         for abstract in abstracts:
#             reviews = Project_Reviews.objects.filter(abstract_id=abstract)
            
#             # Strip path and get the file name
#             abstract_file_name = os.path.basename(abstract.abstract_file_name)
            
            
#             print(abstract_file_name)
            
#             data.append({
#                 'group_no': group.student_group_no,
#                 'abstract_title': abstract.abstract_title,
#                 'abstract_status': abstract.abstract_status,
#                 'guide_message': abstract.guide_message,
#                 'abstract_path': abstract_file_name  # Use the file name without path
#             })
            
#             # Debugging: Print the file name
#             print(abstract_file_name)

#     return render(request, 'view_projects.html', {
#         'data': data,
#         'guide': guide
#     })



# def view_projects(request):
#     # 1. Get the HOD user
#     user_id = request.session.get('user_id')
    
#     hod_user = get_object_or_404(Users, id=user_id)
#     id = hod_user.id
#     print('hod_user', hod_user)
    
    
#     # 2. Get department and course
#     department = hod_user.department_id
#     course = hod_user.course_id

#     # 3. Get all students in the same department and course
#     students = Users.objects.filter(
#         department_id=department,
#         course_id=course,
#         user_role_choice='Student'
#     )

#     # 4. Get student groups where these students belong
#     student_groups = Student_Groups.objects.filter(user_id__in=students)

#     data = []

#     for group in student_groups:
#         # 5. Get abstracts linked to this group
#         abstracts = Abstract.objects.filter(group_id=group)

#         for abstract in abstracts:
#             student = group.user_id
#             guide = Users.objects.filter(
#                 department_id=department,
#                 course_id=course,
#                 user_role_choice='Guide'
#             ).first()  # Adjust if specific guide-to-student mapping exists

#             abstract_file_name = os.path.basename(abstract.abstract_file_name or '')

#             data.append({
#                 'group_no': group.student_group_no,
#                 'abstract_title': abstract.abstract_title,
#                 'abstract_status': abstract.abstract_status,
#                 'guide_message': abstract.guide_message,
#                 'abstract_path': abstract_file_name,
#                 'student_name': student.name,
#                 'guide_name': guide.name if guide else "N/A",
#                 'guide_email': guide.email if guide else "N/A",
#             })

#     return render(request, 'view_projects.html', {
#         'data': data,
#         'hod': hod_user
#     })



def view_projects(request):
    abstracts = Abstract.objects.all()
    data = []

   
    return render(request, 'view_projects.html', {'abstracts': abstracts})
