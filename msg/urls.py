from django.urls import path
from . import views

urlpatterns = [
    path('addMsg',views.addMsg),
    
]
