from django.urls import path
from .views import addsubject,viewsubjects

urlpatterns = [
    path('addSubject',addsubject),
    path('viewSubjects',viewsubjects),
]
