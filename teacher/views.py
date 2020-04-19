from django.shortcuts import render
import re
from base64 import b64encode
from exam.views import database
# Create your views here.
def getpass(a):
    p=""
    for i in a:
        h=chr(ord(i)-10 if(ord(i)>65 and ord(i)<90) else ord(i)+26)
        p+=str(ord(i))+h
    return b64encode(p.encode())
def teacher(request):
    if request.method == "POST":
        print('rahul')
        name=request.POST.get('name')
        number=request.POST.get('number')
        email=request.POST.get('email')
        age=request.POST.get('age')
        experience=request.POST.get('experience')
        gen=request.POST.get('gen')
        s=request.POST.get('s')
        d=request.POST.get('d')
        a=number+"@TP@"+age
        password = getpass(a)
        print(s,d)
        data = {
                'name':name,
                'number':number,
                'email':email,
                'age':age,
                'experience':experience,
                'gen':gen,
                's':s,
                'd':d,
        }
        if(not name.replace(' ','').isalpha()):
            error="Name is invalid"
            data['error']=error
            return render(request,'teacher.html',data)
        elif(s is None):
            error = "Please Select State"
            data['error']=error
            return render(request,'teacher.html',data)
        return render(request,'teacher.html',data)
    else:    
        name=""
        print('rahul11')
        email=""
        data = {
            'name':name,
            'email':email,
            's':'Select State First',
            'error': '',
            'success': '',
            'info': ''
        }
        return render(request,'teacher.html',data)
