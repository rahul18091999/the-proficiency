from django.urls import path
from . import views,edit
urlpatterns = [
    path('addQuestion',views.question),
    path('viewQuestion',views.viewQuestion),
    path('seeQues',views.seeQues),
    path('editQues',views.editQues),
    path('addImage',views.addImage),
    path('edit',edit.edit),
    path('edit1',edit.edit1),
    path('edit3',edit.edit3),
    path('edit2',edit.edit2),


]