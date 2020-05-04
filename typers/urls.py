from django.urls import path
from . import views
urlpatterns = [
    path('viewquestion', views.viewQues),
    path('editProfile', views.editProfile),
]