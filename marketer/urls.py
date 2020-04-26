from django.urls import path
from . import views

urlpatterns = [
    path('editProfile',views.editprofile),
    path('referal',views.referal),
]
