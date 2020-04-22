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

# def checkpermission(url):


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
        number=request.POST.get('phone')
        password=request.POST.get('pass')
        user=request.POST.get('type')
        # usertype=getuserdetail(user)
        
        # idp=userid[0:2]
        # request.session['user']=userid
        # request.session['us']=idp

        if(user=='11'):

            return HttpResponse('Marketers')
        elif(user=='12'):
            teacherdata=database.child('tIds').child(number).get().val()
            if( teacherdata and getpass(password)[2:-1]==teacherdata['pass']):
                request.session['user']=teacherdata['id']
                request.session['us']=user
                return redirect('/home')
            else:
                return render(request,'index.html',{'error':"Please use correct id and password"})
        elif(user=='13'):
            admindata=database.child('aIds').child(number).get().val()
            if( admindata and getpass(password)[2:-1]==admindata['pass']):
                request.session['user']=admindata['id']
                request.session['us']=user
                return redirect('/home')
            else:
                return render(request,'index.html',{'error':"Please use correct id and password"})
        elif(user=='14'):
            typerdata=database.child('tyIds').child(number).get().val()
            if( typerdata and getpass(password)[2:-1]==typerdata['pass']):
                request.session['user']=typerdata['id']
                request.session['us']=user
                return redirect('/typer')
            else:
                return render(request,'index.html',{'error':"Please use correct id and password"})
        else:
            superdata=database.child('sIds').child(number).get().val()
            if( superdata and getpass(password)[2:-1]==superdata['pass']):
                request.session['user']=superdata['id']
                request.session['us']=user
                return redirect('/home')
            else:
                return render(request,'index.html',{'error':"Please use correct id and password"})
    return render(request,'index.html')


def addTeacher(request):
    name=request.GET.get('name')
    return render('/teacher',{'name':name})

