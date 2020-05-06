from django.shortcuts import render

# Create your views here.

def viewNotifications(request):
    return render(request,'./notification/viewNotifications.html')


def addNotifications(request):
    return render(request,'./notification/addNotifications.html')


    