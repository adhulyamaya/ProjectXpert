from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Users, Abstract, Project_Reviews

def course_students_view(request, course_id):
    # Fetch all users (students) enrolled in the course
    students = Users.objects.filter(course_id=course_id)

    # Prepare a list of students with their abstract titles and project statuses
    student_data = []
    for student in students:
        student_group = student.student_groups.all().first()  # Assuming each student belongs to one group
        student_abstract = Abstract.objects.filter(group_id=student_group).first()  # Get the student's abstract
        project_review = Project_Reviews.objects.filter(group_id=student).first()  # Get the student's project review

        student_data.append({
            'name': student.name,
            'email': student.email,
            'student_group': student_group.student_group_no if student_group else None,
            'abstract_title': student_abstract.abstract_title if student_abstract else None,
            'project_status': project_review.project_status if project_review else 'No Review'
        })

    context = {
        'students': student_data,
        'course_id': course_id
    }

    return render(request, 'course_students.html', context)


def project_details(request):
    return render(request, 'course_students.html')