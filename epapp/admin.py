from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model


# Register your models here.
admin.site.register(ModiUser)
admin.site.register(Course)
admin.site.register(CourseStudent)
admin.site.register(CourseComponent)
admin.site.register(CourseAssignment)
admin.site.register(CourseSubmission)
admin.site.register(CourseQuiz)
admin.site.register(CourseQuizQuestion)
admin.site.register(CourseQuizResponse)
admin.site.register(CourseQuizScore)
# admin.site.register(Course)


admin.site.register(Event)