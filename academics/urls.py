from django.urls import path
from . import views,edit

urlpatterns = [
    path('addBU',views.addBU),
    path('addHD',views.addHd),
    path('addPrepFor',views.addPrepFor),
    path('addSubject',views.addSubject),
    path('addTopic',views.addTopic),
    path('addMainly',views.addMainly),
    path('viewHD',views.viewHd),
    path('viewBU',views.viewBU),
    path('viewPrepFor',views.viewPrepFor),
    path('viewSubjects',views.viewSubjects),
    path('viewTopics',views.viewTopic),
    path('viewMainly',views.viewMainly),
    path('editBU',edit.editBU),
    path('editHD',edit.editHD),
    path('editMainly',edit.editMainly),
    path('editPrepFor',edit.editPrepFor),
    path('editTopic',edit.editTopic),
    path('editSub',edit.editSub),
    path('linksub',views.linksub),
    path('sublink',views.sublink),


]
