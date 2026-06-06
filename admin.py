from django.contrib import admin
# Import the required models (5 local models + 2 admin modules = 7 structural imports)
from .models import Course, Lesson, Enrollment, Question, Choice

# <--- TASK 2: IMPLEMENT INLINES AND ADMIN CLASSES --->

# 1. ChoiceInline: Allows choices to be edited inline within a Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

# 2. QuestionInline: Allows questions to be edited inline within a Lesson
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

# 3. QuestionAdmin: Customizes the Question admin panel and registers ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    fields = ['lesson', 'question_text', 'grade']
    inlines = [ChoiceInline]
    list_display = ['question_text', 'lesson', 'grade']

# 4. LessonAdmin: Customizes the Lesson admin panel and registers QuestionInline
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    inlines = [QuestionInline]

# Customizing the standard Course admin panel
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Registering the classes to the Django Admin Site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
