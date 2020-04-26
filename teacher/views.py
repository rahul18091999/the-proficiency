from django.shortcuts import render, redirect
import re
from django.http import HttpResponse

from exam.views import database, getpass, checkpermission, storage
# Create your views here.


def teacher(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    if request.method == "POST":
        # print('rahul')
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        gen = request.POST.get('gen')
        s = request.POST.get('s')
        d = request.POST.get('d')
        userType = request.POST.get('userType')
        data = {
            'name': name,
            'number': number,
            'email': email,
            'age': age,
            'experience': experience,
            'gen': gen,
            's': s,
            'd': d,
        }
        if(not name.replace(' ', '').isalpha()):
            error = "Name is invalid"
            data['error'] = error
            return render(request, 'teacher.html', data)
        elif(len(str(number)) != 10):
            error = "Phone Number is invalid"
            data['error'] = error
            return render(request, 'teacher.html', data)
        elif(email == ''):
            error = "Email is invalid"
            data['error'] = error
            return render(request, 'teacher.html', data)
        elif(s is None):
            error = "Please Select State"
            data['error'] = error
            return render(request, 'teacher.html', data)

        from datetime import datetime
        from random import randint
        time_now = int(datetime.now().timestamp()*100)
        create = request.session['user']

        if userType == "Teacher":
            if (database.child('tIds').child(number).shallow().get().val()):
                error = "Phone Number Already exists"
                data['error'] = error
                return render(request, 'teacher.html', data)

            free = database.child('tIds').child(
                'free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 100001
            database.child('tIds').child(number).update({
                'createdOn': time_now,
                'id': "12"+str(tempid),
                'verify': randint(100000, 999999),
                'pass': getpass(number+"@TP@"+age)[2:-1],
                'createdBy': create
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
            database.child('tIds').update({'free': tempid+1})
            data = {
                'name': '',
                'email': '',

            }
            data['success'] = "Teacher has been added Successfully!"
            data['info'] = number + "@TP@" + age + " and 12" + str(
                tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
            return render(request, 'teacher.html', data)
        elif userType == "Admin":
            if (database.child('aIds').child(number).shallow().get().val()):
                error = "Phone Number Already exists"
                data['error'] = error
                return render(request, 'teacher.html', data)
            free = database.child('aIds').child(
                'free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000

            database.child('aIds').child(number).update(
                {
                    'id': '13'+str(tempid),
                    'createdOn': time_now,
                    'createdBy': create,
                    'pass': getpass(number+"@TP@"+age)[2:-1]
                }
            )
            database.child('admin').child('13'+str(tempid)).child('details').update(
                {
                    'name': name,
                    'phoneNo': number,
                    'age': age,
                }
            )
            database.child('aids').update({'free': tempid+1})
            data = {
                'name': '',
                'email': '',

            }
            data['success'] = "Admin has been added Successfully!"
            data['info'] = number + "@AP@" + age + " and 13" + str(
                tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
            return render(request, 'teacher.html', data)

        elif userType == 'Typer':
            if (database.child('tyIds').child(number).shallow().get().val()):
                error = "Phone Number Already exists"
                data['error'] = error
                return render(request, 'teacher.html', data)
            free = database.child('tyIds').child(
                'free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 100000

            database.child('tyIds').child(number).update(
                {
                    'id': '14'+str(tempid),
                    'createdOn': time_now,
                    'createdBy': create,
                    'pass': getpass(number+"@TP@"+age)[2:-1]
                }
            )
            database.child('typers').child('14'+str(tempid)).child('details').update(
                {
                    'name': name,
                    'phoneNo': number,
                    'age': age,
                }
            )
            database.child('tyIds').update({'free': tempid+1})
            data = {
                'name': '',
                'email': '',

            }
            data['success'] = "Typer has been added Successfully!"
            data['info'] = number + "@TYP@" + age + " and 14" + str(
                tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
            return render(request, 'teacher.html', data)
        elif userType == "Marketer":
            data = {
                'name': '',
                'email': '',

            }
            data['success'] = "Marketer has been added Successfully!"
            data['info'] = number + "@MP@" + age + " and 11" + str(
                tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
            return render(request, 'teacher.html', data)
    else:
        # print(request.session['user'])
        name = ""
        email = ""
        data = {
            'name': name,
            'email': email,
            's': 'Select State First',
            'error': '',
            'success': '',
            'info': ''
        }
        return render(request, 'teacher.html', data)


def viewTeacher(request, typ):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    if typ == "teacher":
        teacherData = database.child('teachers').get()
        print(teacherData)
        l = []
        for i in teacherData:
            print(i.key())
            if(i.key() != 'qBank'):
                l.append(
                    {
                        'tId': i.key(),
                        'name': i.val()['details']['name'],
                        'number': i.val()['details']['phone'],
                        'email': i.val()['details']['email'],
                        's': i.val()['details']['state'],
                        'd': i.val()['details']['city'],
                        'age': i.val()['details']['age'],
                        'experience': i.val()['details']['experience'],
                        'gen': i.val()['details']['gen'],
                    }
                )
        teach = "teach"
        return render(request, 'viewTeacher.html', {'data': l, 'teach': teach})
    elif typ == "typer":
        typerData = database.child('typers').get()
        l = []
        for i in typerData:
            print(i.key())
            if(i.key() != 'qBank'):
                l.append(
                    {
                        'tId': i.key(),
                        'name': i.val()['details']['name'],
                        'number': i.val()['details']['phoneNo'],
                    }
                )
                typ = "typ"
        return render(request, 'viewTeacher.html', {'data': l, 'typ': typ})
    else:
        return render(request, "admin.html")


def viewDashboard(request):
    idd = request.session['user']
    t = database.child('teachers').child(idd).child(
        'reviews').child('dailyExams').get()
    date = []
    for i in t:
        dat = i.key()
        dat = dat[0:2]+'/'+dat[2:4]+'/'+dat[4:]
        s = 0
        l = (len(i.val()))
        for j in i.val():
            s += i.val()[j]['rate']
        date.append({'date': dat, 'rate': s/l})
        #     print(j['rate'])
    # date=[]
    # rate=[]
    # for i in t:
    #     dat=i.key()
    #     date.append(dat[0:2]+'/'+dat[2:4]+'/'+dat[4:])
    #     s=0
    #     l=(len(i.val()))
    #     for j in i.val():
    #         s+=i.val()[j]['rate']
    #     rate.append(s/l)
    # print(date,rate)
    # if(len(date)>7):
    #     date=date[-7:]
    #     rate=rate[-7:]
    # import matplotlib.pyplot as plt
    # plt.plot(date,rate, color='green', linestyle='dashed', linewidth = 3,
    #      marker='o', markerfacecolor='blue', markersize=12)
    # plt.ylim(0,5)
    # # naming the x axis
    # plt.xlabel('Date')
    # # naming the y axis
    # plt.ylabel('Rating')
    # plt.title('Your Performance from '+str(date[0])+' to '+str(date[-1]))
    # plt.savefig('./templates/teacherReviews/'+str(idd)+'.png')

    url = storage.child('teachers').child('20100003.jpg').get_url(1)

    import requests
    import ast
    # import urllib.parse

    #     urllib.parse.quote(query)
    x = requests.get(url)
    try:
        print(ast.literal_eval(x.text)['error'])
        url = "https://firebasestorage.googleapis.com/v0/b/the-proficiency.appspot.com/o/teachers%2F200X200.png?alt=media&token=1"
    except:
        pass
    data = {'data': date, 'url': url}
    return render(request, "teacherreview.html", data)


def rating(request):
    idd = request.session['user']
    t = database.child('teachers').child(idd).child(
        'reviews').child('dailyExams').get()
    date = []
    x = []
    y = []
    if t.val() is not None:
        for i in t:
            dat = i.key()
            dat = dat[0:2]+'/'+dat[2:4]+'/'+dat[4:]
            s = 0
            l = (len(i.val()))
            for j in i.val():
                s += i.val()[j]['rate']
            date.append({'x': dat, 'y': s/l})
            x.append(dat)
            y.append(s/l)
    return render(request, './teacher/reviews.html', {'data': date, 'x': x, 'y': y})


def viewQuestion(request):
    idd = request.session['user']
    t = database.child('teachers').child(idd).child('questions').get()
    data = []
    print(t.val())
    if t.val() is not None:
        for i in t:
            data.append({'qid': i.key(), 'topicid': i.val()['topic']})
    return render(request, './teacher/questions.html', {'data': data})

def editProfile(request):
    iduser = request.session['user']
    i = database.child('teachers').child(iduser).child('details').get()
    from datetime import date
    data=database.child('tIds').child(i.val()["phone"]).child('createdOn').get().val()/100 
    date=date.fromtimestamp(data)
    l = {
        'id': iduser,
        'name': i.val()["name"],
        'age':i.val()["age"],
        'city':i.val()["city"],
        'email':i.val()["email"],
        'experience':i.val()["experience"],
        'gen':i.val()["gen"],
        'phone':i.val()["phone"],
        'state':i.val()["state"],
        'createdOn':date
    }
    if(request.method=="POST"):
        currentpassword=request.POST.get("currentpassword")
        newpassword=request.POST.get("newpassword")
        confirmpassword=request.POST.get("confirmpassword")
        if (currentpassword=="" and newpassword=="" and confirmpassword==""):
            return redirect("/home")
        else:
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './teacher/editProfile.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('tIds').child(i.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './teacher/editProfile.html', {'data': l,'error':"Check Your Current Password"})
                else:
                    database.child('tIds').child(i.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
                    return redirect('/home')
    else:
        
        return render(request, './teacher/editProfile.html', {'data': l})



def referal(request):
    idd = request.session['user']
    data = database.child('share').child('teachers').child(idd).get()
    totalearning = data.val()['earned']
    typea = data.val()['typeA']
    typeb = data.val()['typeB']
    typec = data.val()['typeC']
    code = {'typea': typea['code'],
            'typeb': typeb['code'], 'typec': typec['code']}
    typeatrnc = []
    typebtrnc = []
    typectrnc = []
    if 'trnc' in typea:
        for i in typea['trnc']:
            typeatrnc.append({'trnc': i, 'earn': typea['trnc'][i]})
    if 'trnc' in typeb:
        for i in typeb['trnc']:
            typebtrnc.append({'trnc': i, 'earn': typeb['trnc'][i]})
    if 'trnc' in typec:
        for i in typec['trnc']:
            typectrnc.append({'trnc': i, 'earn': typec['trnc'][i]})
    return render(request, './teacher/referal.html', {'code': code, 'typeatrnc': typeatrnc, 'typebtrnc': typebtrnc, 'typectrnc': typectrnc})