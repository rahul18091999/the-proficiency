from django.urls import path
from . import views,edit
urlpatterns = [
    path('teacher', views.viewteacher),
    path('typer',views.viewtyper),
    path('addUser',views.users),
    path('admin',views.viewmyquestion),
    path('marketer',views.viewmarketer),
    path('editteacher',edit.editteacher),
    path('editmarketer',edit.editMarketer),
    path('edittyper',edit.edittyper),    
    path('viewStu',views.viewStudents),
    path('resendOTP',views.resendOTP),
    
]
