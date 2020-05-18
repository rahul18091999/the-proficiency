from django.urls import path
from . import views


urlpatterns = [
    
    # path('overall',views.overall),
    # path('panda',views.panda)
   
    path('forgetPassword',views.forgotPassword),
    path('newPassword',views.newPassword),
]