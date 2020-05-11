from django.shortcuts import render, redirect
from django.http import HttpResponse
from base64 import b64encode
import pyrebase
config = {
    'apiKey': "AIzaSyBvVgen1TvuoKinJYwvaNH8n7VIACGbqgI",
    'authDomain': "the-proficiency.firebaseapp.com",
    'databaseURL': "https://the-proficiency.firebaseio.com",
    'projectId': "the-proficiency",
    'storageBucket': "the-proficiency.appspot.com",
    'messagingSenderId': "859931947137",
    'appId': "1:859931947137:web:66edfbcbe4489fab789d80"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def checkpermission(r, url):
    try:
        idd = r.session['us']
        l11 = ['/logout','/home','/marketer/referal','/marketer/editProfile']
        l12 = ['/logout','/home','/teacher/viewQuestion','/teacher/rating','/teacher/editProfile','/teacher/referal','/teacher/earning',]
        l13 = ['/logout', '/home','/teacher/addTeacher',
                '/question/addQuestion', '/question/viewQuestion','/user/teacher','/user/typer','/user/addUser']
        l14 = ['/logout', '/home', '/question/addQuestion',
               '/typer/viewquestion','/typer/editProfile']
        l15 = ['/logout', '/home', '/question/addQuestion', '/question/viewQuestion','/user/addUser','/user/teacher','/user/typer','/user/marketer',
        '/academics/addBU','/academics/viewBU','/academics/viewHD','/academics/addHD','/academics/viewPrepFor'
        ,'/academics/addPrepFor','/academics/viewMainly','/academics/addMainly','/academics/viewSubjects','/academics/addSubject',
        '/academics/viewTopics','/academics/addTopic','/exams/addDaily','/exams/addNLE','/exams/viewCoupons','/exams/addCoupon',
        '/banners/addBanner']
        if(idd == '11'):
            if url in l11:
                return 1
            else:
                return 0
        elif(idd == '12'):
            if url in l12:
                return 1
            else:
                return 0
        elif(idd == '13'):
            if url in l13:
                return 1
            else:
                return 0
        elif(idd == '14'):
            if url in l14:
                return 1
            else:
                return 0
        elif(idd == '15'):
            if url in l15:
                return 1
            else:
                return 0
        elif(idd == '16'):
            if url in l16:
                return 1
            else:
                return 0
    except:
        return -1


def getpass(a):
    p = ""
    for i in a:
        h = chr(ord(i)-10 if(ord(i) > 65 and ord(i) < 90) else ord(i)+26)
        p += str(ord(i))+h
    return str(b64encode(p.encode()))

def getname(idd):
    user=getuserdetail(str(idd)[:2])
    username=database.child(user[0]).child(idd).child('details').get().val()['name']
    return username

def getimage(idd):
    user=getuserdetail(str(idd)[:2])
    try:
        url=storage.child(user[0]).child(idd).get_url(1)
        print('rahul')
        import requests
        import ast
        # import urllib.parse
            
        #     urllib.parse.quote(query)
        x = requests.get(url)
        try:
            ast.literal_eval(x.text)['error']
            url="https://firebasestorage.googleapis.com/v0/b/the-proficiency.appspot.com/o/users%2Fteacher.png?alt=media&token=81e94f95-bf4a-4ffb-a98f-eb709aefee14"
        except:
            pass
    except:
         url="https://firebasestorage.googleapis.com/v0/b/the-proficiency.appspot.com/o/users%2Fteacher.png?alt=media&token=81e94f95-bf4a-4ffb-a98f-eb709aefee14"   
    return url

def getuserdetail(userid):
    if(userid == '11'):
        return ['marketers','mIds',1000001]
    elif(userid == '12'):
        return ['teachers', 'tIds', 100001]
    elif(userid == '13'):
        return ['admin', 'aIds', 1001]
    elif(userid == '14'):
        return ['typers', 'tyIds', 100001]
    elif(userid == '15'):
        return ['superAdmin', 'sIds', 1001]


def header(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    else:
        us = request.session['us']
        if(us == '14'):
            return render(request, './typer/dashboard.html')
        elif(us == '15'):
            return render(request, 'index.html')
        elif(us=='12'):
            return render(request, './teacher/dashboard.html')
        elif(us=='13'):
            return render(request, './admin/dashboard.html')
        elif(us=='11'):
            return render(request, './marketer/dashboard.html')


def index(request):
    if(checkpermission(request,request.path)==-1):
        if request.method == 'POST':
            number = request.POST.get('phone')
            password = request.POST.get('pass')
            user = request.POST.get('type')
            # usertype=getuserdetail(user)

            # idp=userid[0:2]
            # request.session['user']=userid
            # request.session['us']=idp
            from datetime import datetime
            if(number and password and user):
                if(user == '11'):

                    marketerdata = database.child('mIds').child(number).get().val()
                    if(marketerdata and getpass(password)[2:-1] == marketerdata['pass']):
                        request.session['name']=database.child('marketers').child(marketerdata['id']).child('details').get().val()['name']
                        request.session['user'] = marketerdata['id']
                        request.session['us'] = user
                        request.session['image']=getimage(marketerdata['id'])
                        database.child('mIds').child(number).update({'lastLogin':int(datetime.now().timestamp()*1000)})
                        return redirect('/home')
                    else:
                        return render(request, 'login.html', {'error': "Please use correct id and password"})
                elif(user == '12'):
                    teacherdata = database.child('tIds').child(number).get().val()
                    if(teacherdata and getpass(password)[2:-1] == teacherdata['pass']):
                        request.session['name']=database.child('teachers').child(teacherdata['id']).child('details').get().val()['name']
                        request.session['user'] = teacherdata['id']
                        request.session['us'] = user
                        request.session['image']=getimage(teacherdata['id'])
                        database.child('tIds').child(number).update({'lastLogin':int(datetime.now().timestamp()*1000)})
                        return redirect('/home')
                    else:
                        return render(request, 'login.html', {'error': "Please use correct id and password"})
                elif(user == '13'):
                    admindata = database.child('aIds').child(number).get().val()
                    if(admindata and getpass(password)[2:-1] == admindata['pass']):
                        request.session['name']=database.child('admin').child(admindata['id']).child('details').get().val()['name']
                        request.session['user'] = admindata['id']
                        request.session['us'] = user
                        request.session['image']=getimage(admindata['id'])
                        database.child('aIds').child(number).update({'lastLogin':int(datetime.now().timestamp()*1000)})
                        return redirect('/home')
                    else:
                        return render(request, 'login.html', {'error': "Please use correct id and password"})
                elif(user == '14'):
                    typerdata = database.child('tyIds').child(number).get().val()
                    if(typerdata and getpass(password)[2:-1] == typerdata['pass']):
                        request.session['name']=database.child('typers').child(typerdata['id']).child('details').get().val()['name']
                        request.session['user'] = typerdata['id']
                        request.session['us'] = user
                        request.session['image']=getimage(typerdata['id'])
                        database.child('tyIds').child(number).update({'lastLogin':int(datetime.now().timestamp()*1000)})
                        return redirect('/home')
                    else:
                        return render(request, 'login.html', {'error': "Please use correct id and password"})
                else:
                    superdata = database.child('sIds').child(number).get().val()
                    if(superdata and getpass(password)[2:-1] == superdata['pass']):
                        request.session['name']=database.child('superAdmin').child(superdata['id']).child('details').get().val()['name']
                        request.session['user'] = superdata['id']
                        request.session['us'] = user
                        request.session['image']=getimage(superdata['id'])
                        database.child('sIds').child(number).update({'lastLogin':int(datetime.now().timestamp()*1000)})
                        return redirect('/home')
                    else:
                        return render(request, 'login.html', {'error': "Please use correct id and password"})
            else:
                return render(request, 'login.html', {'error': "Please enter all the Details"})
        else:
            return render(request, 'login.html')
    else:
        return redirect('/home')


def logout(request):
    if(checkpermission(request, '/logout')!=-1):
        
        
        del request.session['user']
        del request.session['us']
    return redirect('/')


def apiCall(request):
    token = request.GET.get('token')
    next = request.GET.get('next')
    idd=database.child('apiCalls').get().val()[token]
    pre=str(idd)[:2]
    print(idd)
    request.session['name']=database.child('teachers').child(idd).child('details').get().val()['name']
    request.session['user'] = idd
    request.session['us'] = str(idd)[:2]
    request.session['image']=getimage(idd)
    print(token,next)
    return redirect(next)