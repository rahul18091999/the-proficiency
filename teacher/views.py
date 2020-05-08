from django.shortcuts import render, redirect
import re
from django.http import HttpResponse

from exam.views import database, getpass, checkpermission, storage,getimage
# Create your views here.


# def viewDashboard(request):
#     idd = request.session['user']
#     t = database.child('teachers').child(idd).child(
#         'reviews').child('dailyExams').get()
#     date = []
#     for i in t:
#         dat = i.key()
#         dat = dat[0:2]+'/'+dat[2:4]+'/'+dat[4:]
#         s = 0
#         l = (len(i.val()))
#         for j in i.val():
#             s += i.val()[j]['rate']
#         date.append({'date': dat, 'rate': s/l})
#         #     print(j['rate'])
#     # date=[]
#     # rate=[]
#     # for i in t:
#     #     dat=i.key()
#     #     date.append(dat[0:2]+'/'+dat[2:4]+'/'+dat[4:])
#     #     s=0
#     #     l=(len(i.val()))
#     #     for j in i.val():
#     #         s+=i.val()[j]['rate']
#     #     rate.append(s/l)
#     # print(date,rate)
#     # if(len(date)>7):
#     #     date=date[-7:]
#     #     rate=rate[-7:]
#     # import matplotlib.pyplot as plt
#     # plt.plot(date,rate, color='green', linestyle='dashed', linewidth = 3,
#     #      marker='o', markerfacecolor='blue', markersize=12)
#     # plt.ylim(0,5)
#     # # naming the x axis
#     # plt.xlabel('Date')
#     # # naming the y axis
#     # plt.ylabel('Rating')
#     # plt.title('Your Performance from '+str(date[0])+' to '+str(date[-1]))
#     # plt.savefig('./templates/teacherReviews/'+str(idd)+'.png')

#     url = storage.child('teachers').child('20100003.jpg').get_url(1)

#     import requests
#     import ast
#     # import urllib.parse

#     #     urllib.parse.quote(query)
#     x = requests.get(url)
#     try:
#         print(ast.literal_eval(x.text)['error'])
#         url = "https://firebasestorage.googleapis.com/v0/b/the-proficiency.appspot.com/o/teachers%2F200X200.png?alt=media&token=1"
#     except:
#         pass
#     data = {'data': date, 'url': url}
#     return render(request, "teacherreview.html", data)


def rating(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
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
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    idd = request.session['user']
    t = database.child('teachers').child(idd).child('questions').get()
    data = []
    print(t.val())
    if t.val() is not None:
        for i in t:
            data.append({'qid': i.key(), 'topicid': i.val()['topic']})
    return render(request, './teacher/questions.html', {'data': data})


def teacherearning(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    idd = request.session['user']
    data = database.child('teachers').child(idd).get()
    l = []
    tp = database.child('share').child(
        'teachers').child('tp').shallow().get().val()
    if tp is None:
        tp = 20
        database.child('share').child('teachers').update({'tp': 20})
    total = 0
    if 'income' in data.val():
        exams = data.val()['income']['exams']['daily']

        for i in exams:
            dat = i
            dat = dat[0:2]+'/'+dat[2:4]+'/'+dat[4:]
            l.append(
                {
                    'date': dat,
                    'earning': exams[i]['totalSale'],
                    'money': exams[i]['totalSale']/20
                }
            )
            total += exams[i]['totalSale']

    return render(request, './teacher/earning.html', {'data': l, 'total': total})


def editProfile(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    iduser = request.session['user']
    i = database.child('teachers').child(iduser).child('details').get()
    from datetime import date
    data = database.child('tIds').child(
        i.val()["phone"]).child('createdOn').get().val()/100
    date = date.fromtimestamp(data)
    l = {
        'id': iduser,
        'name': i.val()["name"],
        'age': i.val()["age"],
        'city': i.val()["city"],
        'email': i.val()["email"],
        'experience': i.val()["experience"],
        'gen': i.val()["gen"],
        'phone': i.val()["phone"],
        'state': i.val()["state"],
        'createdOn': date
    }
    if(request.method == "POST"):
        currentpassword = request.POST.get("currentpassword")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")
        
        if(request.FILES):
            
            storage.child('/teachers/'+iduser).put(request.FILES["images"])
            request.session['image']=getimage(iduser)
        if (currentpassword != "" or newpassword != "" or confirmpassword != ""):
            if(newpassword != confirmpassword or len(newpassword) < 6):
                return render(request, './teacher/editProfile.html', {'data': l, 'error': "Check Your Password"})
            else:
                current = database.child('tIds').child(
                    i.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1] != current):
                    return render(request, './teacher/editProfile.html', {'data': l, 'error': "Check Your Current Password"})
                else:
                    database.child('tIds').child(i.val()["phone"]).update(
                        {'pass': getpass(newpassword)[2:-1]})
                    return redirect('/home')
        
        return redirect('/home')
    else:

        return render(request, './teacher/editProfile.html', {'data': l})


def referal(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    idd = request.session['user']
    data = database.child('share').child('teachers').child(idd).get()
    if data.val():
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
    return (request, './teacher/referal.html')
