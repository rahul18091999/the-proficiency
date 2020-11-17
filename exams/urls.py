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
    path('viewCouponsTo',views.viewCouponsTo),
    path('viewNleQues',views.viewNleQues),
    path('addAnsKey',views.addAnsKey),
    path('editDaily',views.editDaily),
    path('viewExamStudent',views.viewExamStudent),
    path('viewExamStu',views.viewExamStu),
    path('viewStudentRank',views.viewStudentRank),
    path('viewStudentRankk',views.viewStudentRankk),
    path('viewNleQues2',views.viewNleQues2)

]
