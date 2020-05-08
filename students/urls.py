from django.urls import path
from . import views


urlpatterns = [
    # path('analysis',views.analysis),
    # path('overall',views.overall),
    # path('panda',views.panda)
    path('verify',views.verify),
    path('forgotPassword',views.forgotPassword),
    path('newPassword',views.newPassword),
]