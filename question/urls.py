from django.urls import path
from . import views
urlpatterns = [
    path('addQuestion',views.question),
    path('add',views.addquestion),
    # path('',views.viewTeacher),
]