from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('teachers/', views.teachers, name='teachers'),
    path('students/', views.students, name='students'),

    path('profile/', views.profile, name='profile'),
    
        
    # path('calendar', views.calendar, name='calendar'),
    # path('course/', views.course_all, name='course_all'),
    path('course/<int:pk>/', views.course, name='course'),
    path('course/<int:pk>/delcourse/', views.delcourse, name='delcourse'),
    path('course/<int:pk>/addquiz/', views.addquiz, name='addquiz'),
    path('course/<int:pk>/editquiz/<int:pk2>/', views.editquiz, name='editquiz'),
    path('course/<int:pk>/editquiz/<int:pk2>/delete/', views.delquiz, name='delquiz'),
    path('course/<int:pk>/editquiz/<int:pk2>/addquestion/', views.addquestion, name='addquestion'),
    path('course/<int:pk>/editquiz/<int:pk2>/delquestion/<int:pk3>/', views.delquestion, name='delquestion'),
    
    path('course/<int:pk>/startquiz/<int:pk2>/', views.startquiz, name='startquiz'),
    path('course/<int:pk>/startquiz/<int:pk2>/submit/', views.submitquiz, name='submitquiz'),



    path('enroll/', views.enroll, name='enroll'),
    path('login/', views.loginn, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='signout'),
]
