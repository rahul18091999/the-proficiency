from django.urls import path
from . import views


urlpatterns = [
    path('sendSms',views.createAccount),
    path('send',views.send),
]
