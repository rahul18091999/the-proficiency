from django.urls import path
from . import views
urlpatterns = [
    path('addTeacher',views.teacher),
    path('viewTeacher/<typ>',views.viewTeacher),
    path('viewDashboard',views.viewDashboard),
    path('rating',views.rating),
    path('viewQuestion',views.viewQuestion),
    path('referal',views.referal),
    path('editProfile',views.editProfile),
]