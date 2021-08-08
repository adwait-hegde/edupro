from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5, null=True)
    teacher =  models.ForeignKey(User, on_delete=models.CASCADE)
    enroll = models.CharField(max_length=10, unique=True)

class CourseStudent(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    student =  models.ForeignKey(User, on_delete=models.CASCADE) 

class CourseComponent(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=90)
    desc = models.TextField(max_length=5000, blank=True)

class CourseAssignment(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=90)


class CourseSubmission(models.Model):
    course =  models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    student =  models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/coursesubs/')


#### QUIZ START ####

class CourseQuiz(models.Model):
    course =  models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=90)
    topic = models.CharField(max_length=90)

class CourseQuizQuestion(models.Model):
    quiz =  models.ForeignKey(CourseQuiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=150)
    op1 = models.CharField(max_length=150)
    op2 = models.CharField(max_length=150)
    op3 = models.CharField(max_length=150)
    op4 = models.CharField(max_length=150)
    correct = models.IntegerField()
    points = models.IntegerField()

class CourseQuizResponse(models.Model):
    quizquestion =  models.ForeignKey(CourseQuizQuestion, on_delete=models.CASCADE)
    student =  models.ForeignKey(User, on_delete=models.CASCADE)
    selected = models.IntegerField()

class CourseQuizScore(models.Model):
    quiz =  models.ForeignKey(CourseQuiz, on_delete=models.CASCADE)
    student =  models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.IntegerField()
    
#### QUIZ ENDS ####




class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Reminder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()




class ModiUser(models.Model):
    phno = models.CharField(max_length=20, default='000000')
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.BooleanField(default=False)