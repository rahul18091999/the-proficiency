from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

def header(request):
    return render(request,'admin.html')



def addTeacher(request):
    name=request.GET.get('name')
    return render('/teacher',{'name':name})