from django.urls import path
from . import views,edit
urlpatterns = [
    path('teacher', views.viewteacher),
    path('typer',views.viewtyper),
    path('addUser',views.users),
    path('viewTyper',views.dashboard),
    path('admin',views.viewmyquestion),
    path('marketer',views.viewmarketer),
    path('editteacher',edit.editteacher),
    path('editmarketer',edit.editmarketer),
    path('edittyper',edit.edittyper),
    
]
