from django.urls import path
from . import views
urlpatterns = [
    path('<typ>', views.viewuser),
    path('addUser',views.adduser),
    path('viewTyper',views.dashboard),
]
