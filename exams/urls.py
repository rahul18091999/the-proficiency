from django.urls import path
from . import views


urlpatterns = [
    path('addNLE',views.addNLEs),
    path('addDaily',views.daily),
    path('viewDaily',views.viewDaily),
    path('viewNLEs',views.viewNLEs),
    path('addNLEQues',views.addNLEQues),
    path('viewCoupons',views.viewCoupons),
    path('addCoupon',views.addCoupon),

]
