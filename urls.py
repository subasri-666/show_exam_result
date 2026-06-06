from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route to display the main index page listing all available courses
    path(route='', view=views.CourseListView.as_view(), name='index'),
    
    # Route to display the deep registration panel for user signups
    path('registration/', views.registration_request, name='registration'),
    
    # Routes handling authentication handling profiles
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    
    # Route displaying specific layout properties of selected course IDs
    path('<int:pk>/', view=views.CourseDetailView.as_view(), name='course_details'),
    
    # Route controlling enrollment mappings 
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # <--- CRITICAL LAB REQUIREMENT PATHS --->
    
    # Route to load up the exam question list interface
    path('<int:course_id>/exam/', views.exam, name='exam'),
    
    # Task 6 Endpoint A: Process form submission payloads
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Task 6 Endpoint B: Render specific grade transaction scores
    path('<int:course_id>/submission/<int:submission_id>/show_exam_result/', 
         views.show_exam_result, 
         name='show_exam_result'),
]
