from django.urls import path
from . import views


urlpatterns = [
    path('addNotifications',views.addNotifications),
    path('viewNotifications',views.viewNotifications),
   

]
