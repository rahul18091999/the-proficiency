from django.shortcuts import render,redirect
from django.http import HttpResponse
from base64 import b64encode
import pyrebase
config={
    'apiKey': "AIzaSyBvVgen1TvuoKinJYwvaNH8n7VIACGbqgI",
    'authDomain': "the-proficiency.firebaseapp.com",
    'databaseURL': "https://the-proficiency.firebaseio.com",
    'projectId': "the-proficiency",
    'storageBucket': "the-proficiency.appspot.com",
    'messagingSenderId': "859931947137",
    'appId': "1:859931947137:web:66edfbcbe4489fab789d80"
}
firebase=pyrebase.initialize_app(config)
auth = firebase.auth()
database=firebase.database()
def getpass(a):
    p=""
    for i in a:
        h=chr(ord(i)-10 if(ord(i)>65 and ord(i)<90) else ord(i)+26)
        p+=str(ord(i))+h
    return str(b64encode(p.encode()))

def getuserdetail(userid):
    if(userid == '11'):
        return
    elif(userid == '12'):
        return ['teachers','tIds',100001]
    elif(userid == '13'):
        return ['admin','aIds',1001]
    elif(userid == '14'):
        return ['typers','tyIds',100001]
    elif(userid == '15'):
        return ['superAdmin','sIds',1001]

def header(request):
    return render(request,'admin.html')

def index(request):
    if request.method=='POST':
        userid=request.POST.get('uID')
        password=request.POST.get('pass')
        idp=userid[0:2]
        request.session['user']=userid
        request.session['us']=idp
        if(idp=='11'):
            return HttpResponse('Marketers')
        elif(idp=='12'):
            return HttpResponse('Teacher')
        elif(idp=='13'):
            return redirect('/home')
        elif(idp=='14'):
            return redirect('/typer')
        else:
            return redirect('/')
        return HttpResponse((userid,password))
    return render(request,'index.html')


def addTeacher(request):
    name=request.GET.get('name')
    return render('/teacher',{'name':name})

