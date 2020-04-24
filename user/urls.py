from django.urls import path
from . import views
urlpatterns = [
    path('typ/<typ>', views.viewuser),
    path('addUser',views.users),
    path('viewTyper',views.dashboard),
]
