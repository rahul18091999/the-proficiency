from django.shortcuts import render,redirect
from exam.views import checkpermission


# Create your views here.
def home(request):
    if(not checkpermission(request,request.path)):
        return redirect('/')
    return render(request,'typerNavigator.html')


