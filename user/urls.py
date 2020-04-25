from django.urls import path
from . import views
urlpatterns = [
    path('teacher', views.viewteacher),
    path('typer',views.viewtyper),
    path('addUser',views.users),
    path('viewTyper',views.dashboard),
    path('admin',views.viewmyquestion)
]
