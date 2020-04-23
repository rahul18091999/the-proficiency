from django.urls import path
from . import views
urlpatterns = [
    path('addTeacher',views.teacher),
    path('viewTeacher/<typ>',views.viewTeacher),
    path('viewDashboard/<idd>',views.viewDashboard),
]