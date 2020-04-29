from django.shortcuts import render
from exam.views import database,checkpermission

def editteacher(request):
    return render(request,'./teacher/editProfile.html')


def editmarketer(request):
    return render(request,'./marketer/editProfile.html')

def edittyper(request):
    return render(request,'./typer/editProfile.html')