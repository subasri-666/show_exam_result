from django.shortcuts import render, get_object_or_40000, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission
from django.contrib.auth.decorators import login_required

# ... Keep your existing views like index, course_details, registration, login, etc. ...

# <--- TASK 5: IMPLEMENT show_exam_result AND submit FUNCTIONS --->

@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Renders the exam results page, displaying the calculated score 
    and grading breakdown for a specific user attempt.
    """
    context = {}
    # Fetch the course context
    course = get_object_or_404(Course, pk=course_id)
    # Fetch the specific submission tracking details
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Extract all choices that the user selected during the exam session
    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]
    
    # Calculate scores based on lessons and questions tied to the course
    total_score = 0
    earned_score = 0
    
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            # Utilize the model method to check if the response was completely correct
            if question.is_get_score(selected_ids):
                earned_score += question.grade
                
    # Pass metrics to the dashboard template
    context['course'] = course
    context['submission'] = submission
    context['earned_score'] = earned_score
    context['total_score'] = total_score
    
    return render(request, 'onlinecourse/exam_result.html', context)


@login_required
def submit(request, course_id):
    """
    Processes the submitted HTML exam form, evaluates user responses,
    creates a Submission record, and redirects to the results panel.
    """
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # Ensure the user has an active course subscription/enrollment record
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
        except Enrollment.DoesNotExist:
            return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))
            
        # Collect all checked choice IDs from the POST payload form keys
        # The choice inputs in the template are expected to have name="choice_{{choice.id}}"
        selected_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_ids.append(int(value))
                
        if not selected_ids:
            # If no options were selected, refresh or handle edge case
            return redirect('onlinecourse:exam', course_id=course.id)
            
        # Create a new evaluation transaction submission instance
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Pull matching Choice instances from database using filter query
        selected_choices = Choice.objects.filter(id__in=selected_ids)
        
        # Save structural multi-to-many choices relation map
        submission.choices.set(selected_choices)
        submission.save()
        
        # Redirect directly to avoid form resubmission duplicate loops
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))
        
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))
