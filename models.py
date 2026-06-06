import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Course Model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_with='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_chances = models.IntegerField(default=3)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson Model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


# Enrollment Model (Through table)
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BENEFACTOR = 'benefactor'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BENEFACTOR, 'Benefactor'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=HONOR)
    rating = models.FloatField(default=5.0)


# <--- TASK 1: IMPLEMENT QUESTION, CHOICE, AND SUBMISSION MODELS --->

# 1. Question Model
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="Enter your question here")
    grade = models.IntegerField(default=1)  # Grade point for the question

    # Method to calculate if the selected choices are correct
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        
        if all_answers == selected_correct and selected_incorrect == 0:
            return True
        return False

    def __str__(self):
        return self.question_text


# 2. Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# 3. Submission Model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission by {self.enrollment.user.username} for {self.enrollment.course.name}"
