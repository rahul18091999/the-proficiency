from django.urls import path
from . import views
urlpatterns = [
    path('viewTrnc',views.viewTrans),
    path('seeTrnc',views.seeTrns),
]
