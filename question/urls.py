from django.urls import path
from . import views
urlpatterns = [
    path('addQuestion',views.question),
    path('viewQuestion',views.viewQuestion),
    path('seeQues',views.seeQues),
    path('editQues',views.editQues),


]