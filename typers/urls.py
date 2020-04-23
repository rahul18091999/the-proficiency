from django.urls import path
from . import views
urlpatterns = [
    path('viewquestion/<ide>', views.viewQues),
    path('dashboard',views.dashboard),
]