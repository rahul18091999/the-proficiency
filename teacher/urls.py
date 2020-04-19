from django.urls import path
from . import views
urlpatterns = [
    path('addTeacher',views.teacher),
]