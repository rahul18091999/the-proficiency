from django.urls import path
from . import views


urlpatterns = [
    path('addNLE',views.addNLEs),
    path('addDaily',views.daily),
]
