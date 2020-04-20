from django.urls import path
from .views import addsubject,subject,viewsubjects

urlpatterns = [
    path('',subject),
    path('addsubject',addsubject),
    path('viewSubjects',viewsubjects),
]
