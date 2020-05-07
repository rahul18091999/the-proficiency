from django.urls import path
from . import views
urlpatterns = [
    path('viewTickets',views.viewTickets),
    path('seeTicket',views.seeTicket),
]
