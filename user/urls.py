from django.urls import path
from . import views
urlpatterns = [
    path('/<typ>', views.viewuser),
    path('addUser',views.user),
    path('viewTyper',views.dashboard),
]
