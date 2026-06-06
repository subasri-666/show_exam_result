from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # ... Keep your existing index, course, registration, login, and logout paths here ...
    # Example existing paths:
    # path(route='', view=views.CourseListView.as_as_view(), name='index'),
    # path('<int:pk>/', view=views.CourseDetailView.as_view(), name='course_details'),
    # path('<int:course_id>/enroll/', view=views.enroll, name='enroll'),

    # <--- TASK 6: IMPLEMENT EXAM ROUTING PATHS --->
    
    # Path to render the exam questions for a specific course
    path('<int:course_id>/exam/', views.exam, name='exam'),
    
    # Path to handle the exam form submission payload
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path to display the calculated grading results for a specific submission attempt
    path('<int:course_id>/submission/<int:submission_id>/show_exam_result/', 
         views.show_exam_result, 
         name='show_exam_result'),
]
