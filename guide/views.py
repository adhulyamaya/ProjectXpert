from django.shortcuts import render, redirect
from user_management.models import Users, Student_Groups  # Import the custom Users model if you're using one
from college_info.models import Department, Course
from django.shortcuts import render, redirect, get_object_or_404
from guide.models import TopicSubmission
from project_info.models import Abstract, Project_Reviews, Student_Groups


from user_management.models import Users as UserModel
from django.db.models import Q



def guide_dashboard(request):
    try:
        print('5555')
        user_id = request.session.get('user_id')
        print(user_id)

        if not user_id:
            return redirect('user_management:login')  # Redirect to login if session doesn't have user_id

        # Fetch the user instance from the database
        user = Users.objects.get(id=user_id)

        # Get the guide details (user info, department, course, etc.)
        guide_details = {
            'name': user.name,
            'email': user.email,
            'contact_number': user.contact_number,
            'department': user.department_id.department_name,  # Department Name
            'course': user.course_id.course_name,  # Course Name
            'profile_picture': user.profile_picture.url if user.profile_picture else None,  # Profile picture
            'student_group_no': user.student_groups_set.first().student_group_no if user.student_groups_set.exists() else None,  # Student group number
            'student_group_members': user.student_groups_set.first().members.all() if user.student_groups_set.exists() else []  # Group members
        }

        # Render the guide_dashboard.html template with the guide details
        return render(request, 'guide_dashboard.html', {'guide_details': guide_details})

    except Users.DoesNotExist:
        # Handle case where user is not found
        return render(request, 'guide_dashboard.html', {'error': "Guide details not found."})


def edit_profile_guide(request):
    user_id = request.session.get('user_id')
    print(user_id)

    if not user_id:
        return redirect('user_management:login')

    # Fetch the user instance
    user = get_object_or_404(Users, id=user_id)
    print(user)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.contact_number = request.POST.get('contact_number')

        # Handle Course
        course_name = request.POST.get('course')
        if course_name:
            course_obj = Course.objects.filter(course_name=course_name).first()
            if course_obj:
                user.course_id = course_obj

        # Handle Department
        department_name = request.POST.get('department')
        if department_name:
            department_obj = Department.objects.filter(department_name=department_name).first()
            if department_obj:
                user.department_id = department_obj

        # Handle profile picture update
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture

        user.save()  # Save the updated user info
        
        return redirect('guide:guide_dashboard')  # After saving, redirect

    # Pass current user details to the template
    guide_details = {
        'name': user.name,
        'email': user.email,
        'contact_number': user.contact_number,
        'course': user.course_id.course_name if user.course_id else '',
        'department': user.department_id.department_name if user.department_id else '',
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
    }

    return render(request, 'edit_profile.html', {'guide_details': guide_details})


def submit_topic(request):
    if request.method == 'POST':
        try:
            topic = request.POST.get('topic')
            description = request.POST.get('description') or ''
            date = request.POST.get('date')
            submission_type = request.POST.get('submission_type')

            user_id = request.session.get('user_id')
            print("Session User ID:", user_id)

            user = Users.objects.get(id=user_id)

            print("Received Data:")
            print("Topic:", topic)
            print("Description:", description)
            print("Date:", date)
            print("Submission Type:", submission_type)
            print("User:", user)

            TopicSubmission.objects.create(
                user=user,
                topic=topic,
                description=description,
                date=date,
                submission_type=submission_type,
            )

            # ✅ Render the success page
            return render(request, 'success.html')

        except Exception as e:
            print("Error occurred while submitting topic:", e)

        # On error or after redirect
        return redirect('guide:submit_topic')

    return render(request, 'announcement.html')



def project_ranking(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'error.html', {'message': 'User not found in session.'})

    try:
        guide = Users.objects.select_related('course_id', 'department_id').get(id=user_id)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'Guide not found.'})

    course = guide.course_id
    department = guide.department_id

    # Fetch all students in the same course
    students = Users.objects.filter(course_id=course, user_role_choice='student')

    # Fetch all student groups associated with these students
    student_groups = Student_Groups.objects.filter(user_id__in=students)

    # Fetch all abstracts from these student groups
    abstracts = Abstract.objects.filter(group_id__in=student_groups).select_related('group_id')

    # Pre-fetch related project reviews in a dictionary grouped by abstract ID
    reviews_qs = Project_Reviews.objects.filter(abstract_id__in=abstracts)
    project_reviews = {}
    for review in reviews_qs:
        project_reviews.setdefault(review.abstract_id_id, []).append(review)

    context = {
        'abstracts': abstracts,
        'project_reviews': project_reviews,
    }

    return render(request, 'project_ranking.html', context)



def handle_project_action(request, project_id):
    # Fetch the project (abstract) using the provided project ID
    project = get_object_or_404(Abstract, id=project_id)

    # Check if the request is a POST request to handle the action
    if request.method == 'POST':
        action = request.POST.get('action')  # Get the action (accept, reject, hold)
        remarks = request.POST.get('remarks')  # Get the optional remarks

        # Check if action is provided and is valid
        if action not in ['accept', 'reject', 'hold']:
            return redirect('project_ranking')  # Redirect back to the project ranking page

        # Update the abstract status based on the selected action
        if action == 'accept':
            project.abstract_status = 'ACCEPTED'
        elif action == 'reject':
            project.abstract_status = 'REJECTED'
        elif action == 'hold':
            project.abstract_status = 'ON_HOLD'

        # Save the remarks if any
        if remarks:
            project.guide_message = remarks

        # Save the updated project
        project.save()

        # Create or update project review (optional)
        Project_Reviews.objects.create(
            abstract_id=project,
            review_date=request.POST.get('review_date', None),  # You can handle review date as needed
            feedback=remarks,
            project_status=project.abstract_status,
            review_choices=action
        )

        # Show a success message and redirect to the project ranking page
        return redirect('project_ranking')  # Redirect back to the project ranking page

    # If the request is not POST, redirect back to the project ranking page
    return redirect('project_ranking')