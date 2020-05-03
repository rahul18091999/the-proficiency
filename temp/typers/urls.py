from django.urls import path
from . import views
urlpatterns = [
    path('viewquestion', views.viewQues),
    path('dashboard',views.dashboard),
    path('editProfile', views.editProfile),
]