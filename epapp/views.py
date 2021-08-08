from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
# from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def loginn(request):
    # return render(request, 'epapp/login.html')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Wrong credentials,Please try again !")
            return redirect('/login/')
    else:
        return render(request, 'epapp/login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        username = request.POST.get('username')
        phnumber = request.POST.get('phnumber')
        isteacher = request.POST.get('isteacher')
        password = request.POST.get('password')
        print(name,password,username,phnumber,isteacher)
        try:
            user2 = User.objects.create_user(username=username, password=password)
            user_details = ModiUser(user=user2,phno=phnumber,teacher=isteacher=='teacher')
            user_details.save()
            
        except Exception as e:
            messages.error(request,e)
        return redirect('/login/')

def signout(request):
	logout(request)
	messages.success(request,'Successfully logged out')
	return redirect('/login/')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            courses = Course.objects.filter(teacher=user)
            return render(request, 'epapp/teacher_dashboard.html',{'courses':courses})
        else:
            courses = CourseStudent.objects.filter(student=user)
            return render(request, 'epapp/student_dashboard.html',{'courses':courses})
    messages.error(request,"Please Login or SignUp !")
    return redirect('/login/')

def home(request):
    return render(request, 'epapp/home.html')

def addcourse(request):
    if request.method == 'POST':
        name = request.POST.get('coursename')
        code = request.POST.get('code')
        enroll = request.POST.get('enrollmentkey')
        # print(name,code,enroll)
        key = Course.objects.filter(enroll=enroll)
        print(len(key))
        if len(key)>0:
            messages.error(request,"Please keep some other Enrollment key..!")
        else:
            new_course = Course(name=name, code=code,enroll=enroll,teacher=request.user)
            new_course.save()
            messages.success(request,"Course added Successfully!")
        return redirect('/dashboard/')


def enroll(request):
    if request.method == 'POST':
        code = request.POST.get('enrollmentkey')
        key = Course.objects.filter(enroll=code)
        print(code,key)
        if len(key)==0:
            messages.error(request,"Please check your Enrollment key..!")
        else:
            if CourseStudent.objects.filter(course = key[0], student=request.user).exists():
                messages.error(request,"You are already Enrolled..!")
            else:
                csmap = CourseStudent(course = key[0], student=request.user)
                csmap.save()
                messages.success(request,"You are Enrolled Successfully..!")
        return redirect('/dashboard/')

def teachers(request):
    if request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if not user_details.teacher:
                csmap = CourseStudent.objects.filter(student=request.user)
                # teachers = set()
                teachers=[]
                for i in csmap:
                    temp = (i.course, ModiUser.objects.get(user=i.course.teacher))
                    teachers.append(temp)
                    # teachers.add(i.course.teacher)
                # teachers = list(teachers)
                return render (request, 'epapp/teachers.html',{'teachers':teachers})


def students(request):
    if request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if user_details.teacher:
                courses = Course.objects.filter(teacher=user)
                # csmap = CourseStudent.objects.filter(student=request.user)
                # teachers = set()
                allcourse=[]
                # allstudents=[]
                for c in courses:
                    # allcourse.append(c)
                    tmain=[c]
                    temp = []
                    csmap = CourseStudent.objects.filter(course=c)
                    for maps in csmap:
                        temp.append(ModiUser.objects.get(user=maps.student))
                    tmain.append(temp)
                    allcourse.append(tmain)
                print(allcourse)

                    # teachers.add(i.course.teacher)
                # teachers = list(teachers)
                return render (request, 'epapp/students.html',{"allcourse":allcourse})



def course (request, pk):
    if request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if user_details.teacher:
                try:
                    course = Course.objects.get(pk=pk)
                    if course.teacher==user:
                        csmap = CourseStudent.objects.filter(course=course)
                        quizes = CourseQuiz.objects.filter(course=course)
                        students = []
                        for s in csmap:
                            students.append(ModiUser.objects.get(user=s.student))
                        return render(request, 'epapp/teachercourse.html', {'quizes':quizes,'students':students})
                    else:
                        messages.error(request,"You are not the course faculty..")
                except:
                    messages.error(request,"Course no longer available..")
            else:
                try:
                    course = Course.objects.get(pk=pk)
                    if CourseStudent.objects.filter(course=course,student=user).exists():
                        quizes = CourseQuiz.objects.filter(course=course)
                        resp = []
                        for quiz in quizes:
                            print(quiz,user)
                            qs = CourseQuizScore.objects.filter(quiz=quiz,student=user)
                            score = 'N.A.'   
                            if qs.exists():
                                score = qs[0].marks  
                            resp.append([quiz,score])
                        return render(request,'epapp/studentcourse.html', {'quizes':resp})
                    else:
                        messages.error(request,"You are not enrolled..")
                except:
                    messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')
    else:
        return redirect('/login/')

def delcourse(request,pk):
    if request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if user_details.teacher:
                try:
                    course = Course.objects.get(pk=pk)
                    if course.teacher==user:
                        Course.objects.filter(pk=pk).delete()
                    else:
                        messages.error(request,"You are not the course faculty..")
                except:
                    messages.error(request,"Course no longer available..")
            else:
                try:
                    course = Course.objects.get(pk=pk)
                    if CourseStudent.objects.filter(course=course,student=user).exists():
                        CourseStudent.objects.filter(course=course,student=user).delete()
                    else:
                        messages.error(request,"You are not enrolled..")
                except:
                    messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')
    else:
        return redirect('/login/')

def startquiz(request,pk,pk2):
    if request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if not user_details.teacher:
                # return render(request,'epapp/studentquiz.html')
                try:
                    course = Course.objects.get(pk=pk)
                    if CourseStudent.objects.filter(course=course,student=user).exists():
                        quiz = CourseQuiz.objects.get(pk=pk2)
                        questions = CourseQuizQuestion.objects.filter(quiz=quiz)
                        print("   QUIZES    ",quiz)
                        return render(request,'epapp/studentquiz.html', {'questions':questions})
                    else:
                        messages.error(request,"You are not enrolled..")
                except:
                    messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')
    else:
        return redirect('/login/')

def submitquiz(request,pk,pk2):
    if request.method == 'POST'and request.user.is_authenticated:
            user = request.user
            user_details = ModiUser.objects.get(user=user)
            if not user_details.teacher:
                try:
                    course = Course.objects.get(pk=pk)
                    if CourseStudent.objects.filter(course=course,student=user).exists():
                        quiz = CourseQuiz.objects.get(pk=pk2)
                        questions = CourseQuizQuestion.objects.filter(quiz=quiz)
                        score = 0
                        for question in questions:
                            response = request.POST.get('question'+str(question.pk))
                            print('      RESPONSE    ',response)
                            response = int(response)
                            if response is None:
                                response = 0
                            if question.correct == response:
                                score += question.points
                            print('      SCORE    ',score)
                            sub = CourseQuizResponse(quizquestion=question,student=user,selected=response)
                            sub.save()
                        finalscore = CourseQuizScore(quiz=quiz,student=user,marks=score)
                        finalscore.save()
                        print('      SCORE    ',score)

                        # print("   QUIZES    ",quiz)
                        return redirect('course',pk=pk)
                    else:
                        messages.error(request,"You are not enrolled..")
                except:
                    messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')
    else:
        return redirect('/login/')


def addquiz(request,pk):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            try:
                course = Course.objects.get(pk=pk)
                if course.teacher==user:
                    title = request.POST.get('quiztitle')
                    topic = request.POST.get('quiztopic')
                    newquiz = CourseQuiz(course=course, title=title,topic=topic)
                    newquiz.save()
                    rd = '/course/'+str(pk)+'/'
                    return redirect(rd)
                else:
                    messages.error(request,"You are not the course faculty..")
            except:
                messages.error(request,"Course no longer available..")
    return redirect('/dashboard/') 


def editquiz(request,pk,pk2):
    if request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            try:
                course = Course.objects.get(pk=pk)
                if course.teacher==user:
                    # newquiz = CourseQuiz(course=course, title=title,topic=topic)
                    # newquiz.save()
                    quiz = CourseQuiz.objects.get(pk=pk2)
                    questions = CourseQuizQuestion.objects.filter(quiz=quiz)
                    responses = CourseQuizScore.objects.filter(quiz=quiz)
                    
                    return render(request, 'epapp/teacherquiz.html', {'questions':questions, 'responses':responses})
                else:
                    messages.error(request,"You are not the course faculty..")
            except:
                messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')  

def delquiz(request,pk,pk2):
    if request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            try:
                course = Course.objects.get(pk=pk)
                if course.teacher==user:
                    CourseQuiz.objects.filter(pk=pk2).delete()
                    return redirect('course',pk=pk)
                else:
                    messages.error(request,"You are not the course faculty..")
            except:
                messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')  


def addquestion(request,pk,pk2):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            try:
                course = Course.objects.get(pk=pk)
                if course.teacher==user:
                    quiz = CourseQuiz.objects.get(pk=pk2)
                    # questions = CourseQuizQuestion.objects.filter(quiz=quiz)
                    question = request.POST.get('question')
                    op1 = request.POST.get('option1')
                    op2 = request.POST.get('option2')
                    op3 = request.POST.get('option3')
                    op4 = request.POST.get('option4')
                    correct = request.POST.get('correctoption')
                    points = request.POST.get('points')
                    print(op1,op2,op3)
                    newqq = CourseQuizQuestion(quiz=quiz,question=question,op1=op1,op2=op2,op3=op3,op4=op4,correct=correct,points=points)
                    newqq.save()
                    return redirect('editquiz',pk=pk,pk2=pk2)
                else:
                    messages.error(request,"You are not the course faculty..")
            except:
                messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')    


def delquestion(request,pk,pk2,pk3):
    if request.user.is_authenticated:
        user = request.user
        user_details = ModiUser.objects.get(user=user)
        if user_details.teacher:
            try:
                course = Course.objects.get(pk=pk)
                if course.teacher==user:
                    quiz = CourseQuiz.objects.get(pk=pk2)
                    CourseQuizQuestion.objects.filter(pk=pk3).delete()
                    
                    return redirect('editquiz',pk=pk,pk2=pk2)
                else:
                    messages.error(request,"You are not the course faculty..")
            except:
                messages.error(request,"Course no longer available..")
            return redirect('/dashboard/')    

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'epapp/profile.html')
    else:
        return redirect('')