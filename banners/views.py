from django.shortcuts import render

# Create your views here.
def addBanner(request):
    return render(request,'./banners/addBanner.html')