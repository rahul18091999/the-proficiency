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
    return str(b64encode(p.encode()))
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
        elif(len(str(number))!=10 ):
            error="Phone Number is invalid"
            data['error']=error
            return render(request,'teacher.html',data)
        elif(email==''):
            error="Email is invalid"
            data['error']=error
            return render(request,'teacher.html',data)
        elif(s is None):
            error = "Please Select State"
            data['error']=error
            return render(request,'teacher.html',data)
        if (database.child('tIds').child(number).shallow().get().val()):
            error = "Phone Number Already exists"
            data['error']=error
            return render(request,'teacher.html',data)
        else:
            if(database.child('tIds').child('free').shallow().get().val()):
                tempid=database.child('tIds').child('free').shallow().get().val()
            else:
                tempid=100001
            import time
            from datetime import datetime,timezone
            import pytz
            from random import randint
            print()
            
            time_now=int(datetime.now().timestamp()*100)
            
            print(time_now)
            database.child('tIds').child(number).update({
                'createsOn':time_now,
                'id':"12"+str(tempid),
                'verify':randint(100000,999999),
                'pass':getpass(number+"@TP@"+age)[2:-1]
            })
            database.child('teachers').child("12"+str(tempid)).child('details').update(
                {
                    'name': name,
                    'age': age,
                    'state': s,
                    'city': d,
                    'experience': experience,
                    'phone': number,
                    'email': email,
                    'gen': gen
                }
            )
            database.child('tIds').update({'free':tempid+1})
            data = {
                'name':'',
                'email':'',
                
        }
            data['success']="Teacher has been added Successfully!"
            data['info']= number + "@TP@" + age + " and 12" + str(tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ")+ name 
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
