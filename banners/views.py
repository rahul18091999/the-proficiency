from django.shortcuts import render
from exam.views import storage
# Create your views here.
def addBanner(request):
    try:
        url1=storage.child('banners').child(1).get_url(1)
        url2=storage.child('banners').child(2).get_url(1)
        url3=storage.child('banners').child(3).get_url(1)
        url4=storage.child('banners').child(4).get_url(1)
        url5=storage.child('banners').child(5).get_url(1)
        
    except:
        url="https://firebasestorage.googleapis.com/v0/b/the-proficiency.appspot.com/o/logo%2FProfile%20Pic.png?alt=media&token=f5efb3c0-394e-4c28-9442-d061e1204e9b"
        url1 = url
        url2 = url
        url3 = url
        url4 = url
        url5 = url

    return render(request,'./banners/addBanner.html',{'img1':url1,'img2':url2,'img3':url3,'img4':url4,'img5':url5})