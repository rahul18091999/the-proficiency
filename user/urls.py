from django.urls import path
from . import views
urlpatterns = [
    path('teacher', views.viewteacher),
    path('typer',views.viewtyper),
    path('addUser',views.users),
    path('viewTyper',views.dashboard),
    path('admin',views.viewmyquestion),
    path('marketer',views.viewmarketer),
    path('acedemics/addBU',views.addBU),
    path('acedemics/',views.addHd),
    path('acedemics/',views.viewHd),
    path('acedemics/',views.viewBU),
]
