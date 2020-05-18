from django.urls import path
from . import views
urlpatterns = [
    path('rating',views.rating),
    path('viewQuestion',views.viewQuestion),
    path('earning',views.teacherearning),
    path('referal',views.referal),
    path('editProfile',views.editProfile),
    path('tickets',views.tickets),
]