from django.shortcuts import render, redirect
from exam.views import database, checkpermission, getpass
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.


def getcode(typ):
    import random
    import string
    temp = ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=3))
    if(typ == 'a'):
        return temp
    elif(typ == 'b'):
        if(temp == typea):
            getcode('b')
        else:
            return temp
    elif(typ == 'c'):
        if(temp == typea or temp == typeb):
            getcode('c')
        else:
            return temp

def users(request):
    global typea, typeb, typec
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    else:
        menu = database.child('menu').get()
        menuList = []
        for i in menu:
            if i.key()!="free":
                menuList.append({'id':i.key(),'name':i.val()['name']})
        if request.method == "POST":
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
                'menu':menuList,
                'd': d,
            }
            if(not name.replace(' ', '').isalpha()):
                error = "Name is invalid"
                data['error'] = error
                return render(request, './users/addUser.html', data)
            elif(len(str(number)) != 10):
                error = "Phone Number is invalid"
                data['error'] = error
                return render(request, './users/addUser.html', data)
            elif(email == ''):
                error = "Email is invalid"
                data['error'] = error
                return render(request, './users/addUser.html', data)
            elif(s is None):
                error = "Please Select State"
                data['error'] = error
                return render(request, './users/addUser.html', data)
            elif(userType is None):
                error = "Please Select User Type"
                data['error'] = error
                return render(request, './users/addUser.html', data)
            from datetime import datetime
            from random import randint
            time_now = int(datetime.now().timestamp()*1000)
            create = request.session['user']

            if userType == "Teacher":
                
                if (database.child('tIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/addUser.html', data)

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
                database.child('share').child('teachers').child('12'+str(tempid)).update(
                    {
                        'earned': '0'
                    }
                )

                typea = getcode('a')
                typeb = getcode('b')
                typec = getcode('c')

                database.child('share').child('teachers').child('12'+str(tempid)).child('typeA').update(
                    {
                        'code': "12"+str(tempid)+str(typea)
                    }
                )

                database.child('share').child('teachers').child('12'+str(tempid)).child('typeB').update(
                    {
                        'code': "12"+str(tempid)+str(typeb)
                    }
                )

                database.child('share').child('teachers').child('12'+str(tempid)).child('typeC').update(
                    {
                        'code': "12"+str(tempid)+str(typec)
                    }
                )
                database.child('tIds').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',
                'menu':menuList,

                }
                
                d=database.child('email').child('registration').shallow().get().val()
                d = d.replace('[Full Name]',name)
                d = d.replace('[USER ID]',"12"+str(tempid))
                d = d.replace('[phone number]',number)

                d = d.replace('[password]',number+"@TP@"+age)

                send_mail(subject="account",
                message='None',
                        html_message = d ,
                        
                            from_email='Registration<no-reply@the-proficiency.com>',
                            recipient_list=[email])
                data['success'] = "Teacher has been added Successfully!"
                data['info'] = number + "@TP@" + age + "is the password and 12" + str(
                    tempid) + " is the ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)
            elif userType == "Admin":
                permission = []
                for i in menuList:
                    permissions = request.POST.get(i["id"])
                    if permissions:
                        permission.append(permissions)
                
                if (database.child('aIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/addUser.html', data)
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
                        'pass': getpass(number+"@TP@"+age)[2:-1],
                        'permissions':permission
                    }
                )
                database.child('admin').child('13'+str(tempid)).child('details').update(
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
                database.child('aIds').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',

                }
                d=database.child('email').child('registration').shallow().get().val()
                d = d.replace('[Full Name]',name)
                d = d.replace('[USER ID]',"13"+str(tempid))
                print(d.find('[phone number'))
                d = d.replace('[phone number]',number)
                print(d.find('[phone number'))

                d = d.replace('[password]',number+"@TP@"+age)

                send_mail(subject="account",
                message='None',
                        html_message = d ,
                            from_email='Registration<no-reply@the-proficiency.com>',
                            recipient_list=[email])
                data['success'] = "Admin has been added Successfully!"
                data['info'] = number + "@TP@" + age + "is the password and 13" + str(
                    tempid) + " is the ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)

            elif userType == 'Typer':
                print("wxx")
                if (database.child('tyIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/addUser.html', data)
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
                        'age': age,
                        'state': s,
                        'city': d,
                        'experience': experience,
                        'phone': number,
                        'email': email,
                        'gen': gen
                    }
                )
                database.child('tyIds').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',
                'menu':menuList,

                }
                d=database.child('email').child('registration').shallow().get().val()
                d = d.replace('[Full Name]',name)
                d = d.replace('[USER ID]',"14"+str(tempid))
                print(d.find('[phone number'))
                d = d.replace('[phone number]',number)
                print(d.find('[phone number'))

                d = d.replace('[password]',number+"@TP@"+age)

                send_mail(subject="account",
                message='None',
                        html_message = d ,
                            from_email='Registration<no-reply@the-proficiency.com>',
                            recipient_list=[email])
                data['success'] = "Typer has been added Successfully!"
                data['info'] = number + "@TP@" + age + "is the password and 14" + str(
                    tempid) + " is the ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)
            elif userType == "Marketer":
                if (database.child('mIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/addUser.html', data)
                free = database.child('mIds').child(
                    'free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 100000

                database.child('mIds').child(number).update(
                    {
                        'id': '11'+str(tempid),
                        'createdOn': time_now,
                        'createdBy': create,
                        'pass': getpass(number+"@TP@"+age)[2:-1]
                    }
                )
                database.child('marketers').child('11'+str(tempid)).child('details').update(
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

                teachers = database.child('share').child('marketers').child('11'+str(tempid)).update(
                    {
                        'earned': '0'
                    }
                )

                typea = getcode('a')
                typeb = getcode('b')
                typec = getcode('c')

                database.child('share').child('marketers').child('11'+str(tempid)).child('typeA').update(
                    {
                        'code': "11"+str(tempid)+str(typea)
                    }
                )

                database.child('share').child('marketers').child('11'+str(tempid)).child('typeB').update(
                    {
                        'code': "11"+str(tempid)+str(typeb)
                    }
                )

                database.child('share').child('marketers').child('11'+str(tempid)).child('typeC').update(
                    {
                        'code': "11"+str(tempid)+str(typec)
                    }
                )

                database.child('mIds').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',
                'menu':menuList,

                }
                d=database.child('email').child('registration').shallow().get().val()
                d = d.replace('[Full Name]',name)
                d = d.replace('[USER ID]',"11"+str(tempid))
                d = d.replace('[phone number]',number)

                d = d.replace('[password]',number+"@TP@"+age)

                send_mail(subject="account",
                message='None',
                        html_message = d ,
                            from_email='Registration<no-reply@the-proficiency.com>',
                            recipient_list=[email])
                data['success'] = "Marketer has been added Successfully!"
                data['info'] = number + "@MP@" +"is the password and 11" + str(
                    tempid) + " is the ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)

        else:
            
            name = ""
            email = ""
            data = {
                'name': name,
                'email': email,
                's': 'Select State First',
                'error': '',
                'success': '',
                'info': '',
                'menu':menuList,
            }
            return render(request, './users/addUser.html', data)


def viewteacher(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    teacherData = database.child('teachers').get()
    # if teacherData:
    
    l = []
    if(teacherData.val()):
        for i in teacherData:
            
            if(i.key() != 'qBank'):
                print(i.key())
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
    return render(request, './users/teachersList.html', {'data': l, 'type': 'teacher'})


def viewtyper(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
        # try:
    typerData = database.child('typers').get()
    l = []
    if typerData.val():
        for i in typerData:
            print(i.key())
            if(i.key() != 'qBank'):
                l.append(
                    {
                        'tId': i.key(),
                        'name': i.val()['details']['name'],
                        'number': i.val()['details']['phone'],
                        'state': i.val()['details']['state'],
                        'city': i.val()['details']['city'],
                    }
                )
    return render(request, './users/typersList.html', {'data': l, 'type': 'typer'})


def viewmarketer(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    marketerData = database.child('marketers').get()
    l = []
    if marketerData.val():
        for i in marketerData:
            print(i.key())
            l.append(
                {
                    'tId': i.key(),
                    'name': i.val()['details']['name'],
                    'number': i.val()['details']['phone'],
                    'state': i.val()['details']['state'],
                    'city': i.val()['details']['city'],
                }
            )
    return render(request, './users/marketerlist.html', {'data': l, 'type': 'typer'})


def viewmyquestion(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    id1 = request.session['us']
    if id1 == "15":
        id = request.session['user']
        adminQues = database.child['superAdmin'].child[id].child['questionsAdded'].get(
        )
        l = []
        for i in adminQues:
            l.append(
                {
                    'id': i.key(),
                    'by': id
                }
            )
        return render(request, 'viewQuestyper.html', {'question': l})
    elif id1 == "13":
        id = request.session['user']
        adminQues = database.child['admin'].child[id].child['questionsAdded'].get(
        )
        l = []
        for i in adminQues:
            l.append(
                {
                    'id': i.key(),
                    'by': id
                }
            )
    return render(request, 'viewQuestyper.html', {'question': l})


def editprofile(request):
    idd = request.GET.get('id')
    marketerdata = database.child('marketers').child(
        idd).child('details').get()
    from datetime import date
    data = database.child('mIds').child(
        marketerdata.val()["phone"]).child('createdOn').get().val()/1000
    date = date.fromtimestamp(data)
    l = {
        'id': idd,
        'name': marketerdata.val()["name"],
        'age': marketerdata.val()["age"],
        'city': marketerdata.val()["city"],
        'email': marketerdata.val()["email"],
        'experience': marketerdata.val()["experience"],
        'gen': marketerdata.val()["gen"],
        'phone': marketerdata.val()["phone"],
        'state': marketerdata.val()["state"],
        'createdOn': date
    }
    if(request.method == "POST"):
        currentpassword = request.POST.get("currentpassword")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")
        name = request.POST.get('name')
        number = request.POST.get('number')
        mail = request.POST.get('email')
        sate = request.POST.get('state')
        city = request.POST.get('city')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        if (currentpassword == "" and newpassword == "" and confirmpassword == ""):
            if (number == marketerdata.val()["phone"]):
                database.child('marketers').child(idd).child('details').update(
                    {
                        'name': name,
                        'age': age,
                        'city': city,
                        'email': mail,
                        'experience': experience,
                        'gen': marketerdata.val()["gen"],
                        'phone': marketerdata.val()["phone"],
                        'state': sate,
                    }
                )
                return redirect('/user/editMarketer')

            else:
                if (database.child('mIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './marketer/editProfile.html', data)
                else:
                    from random import randint
                    da = database.child('mIds').child(marketerdata.val()[
                        "phone"]).child('createdBY').get().val()
                    database.child('mIds').child(number).update({
                        'createdOn': data,
                        'id': idd,
                        'verify': randint(100000, 999999),
                        'pass': getpass(number+"@TP@"+age)[2:-1],
                        'createdBy': da,
                    })
                    database.child('mIds').child(
                        marketerdata.val()['phone']).remove()
                    database.child('marketers').child(idd).child('details').update(
                        {
                            'name': name,
                            'age': age,
                            'state': sate,
                            'city': city,
                            'experience': experience,
                            'phone': number,
                            'email': mail,
                            'gen': marketerdata.val()["gen"]
                        }
                    )
                    return redirect('/user/editMarketer')
        else:
            if(newpassword != confirmpassword or len(newpassword) < 6):
                return render(request, './marketer/editProfile.html', {'data': l, 'error': "Check Your Password"})
            else:
                current = database.child('mIds').child(
                    marketerdata.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1] != current):
                    return render(request, './marketer/editProfile.html', {'data': l, 'error': "Check Your Current Password"})
                else:
                    database.child('mIds').child(marketerdata.val()["phone"]).update(
                        {'pass': getpass(newpassword)[2:-1]})
                    return redirect('/home')
    else:
        return render(request, './marketer/editProfile.html', {'data': l})






    
def viewStudents(request):
    students = database.child('users').get()
    ids = database.child('ids').get().val()
    l=[]
    from datetime import datetime
    for i in students:
        l.append(
            {
                'id': i.key(),
                'name': i.val()['details']['name'],
                'parent': i.val()['details']['parent'],
                'phone': i.val()['details']['phone'],
                'verify':ids[i.val()['details']['phone']]['verify'],
                'createdOn':datetime.fromtimestamp(int(ids[i.val()['details']['phone']]['createdOn'])/1000),
                'wallet':i.val()['wallet']['balance'] if 'wallet' in i.val() and 'balance' in i.val()['wallet'] else '-'
            }
        )
    return render(request,'./users/viewStu.html',{'data': l})


def resendOTP(request):
    idd=request.GET.get('id')
    data = database.child('ids').child(idd).get().val()
    if data['verify']:
        import requests
        import urllib.parse
        msgdata = database.child('sms').get().val()

        verify = urllib.parse.quote(msgdata['msg']['verification'])

        link = "http://sms.whybulksms.com/api/sendhttp.php?authkey="+msgdata['key']+"&mobiles="+idd+"&message="+verify+str(data['verify'])+"&sender="+msgdata['sndrID']+"&route=4"
        requests.get(link)
    return redirect('/user/viewStu')

def addMoney(request):
    idd = request.GET.get('id')
    print(idd)
    if(request.method=="POST"):
        amount = int(request.POST.get('amount'))
        from datetime import datetime
        from exam.views import getuserdetail
        us = getuserdetail(request.session['us'])
        print(datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
        if amount:
            userData = database.child('users').child(idd).get().val()
            
            time_now = int(datetime.now().timestamp()*1000)
            trncID = idd+str(time_now)
            database.child(us[0]).child(request.session['user']).child('trnc').child(idd).child(trncID).update({
                "BANKTXNID" : "",
                "CURRENCY" : "INR",
                "CUST_ID" : userData['details']['name']+"@"+idd,
                "EMAIL" : "userInfo@tp.com",
                "MID" : "FbFRgc66424314189642CT",
                "MOBILE_NO" : userData['details']['phone'],
                "ORDERID" : trncID,
                "ORDER_ID" : trncID,
                "RESPCODE" : "141",
                "RESPMSG" : "Txn Conplete By Calling team",
                "STATUS" : "TXN_SUCCESS",
                "TXNAMOUNT" : amount,
                "TXNDATE" : datetime.now().strftime("%Y-%m-%d %H.%M.%S"),
                "TXNID" : "20200623111212800110168559732604329CT",
                "TXN_AMOUNT" : amount,
                "cmnts" : "By Calling Team",
                "coupon" : False,
                "sp" : amount*6
            })

            database.child('trnc').child(trncID).update({
                "BANKTXNID" : "",
                "CURRENCY" : "INR",
                "CUST_ID" : userData['details']['name']+"@"+idd,
                "EMAIL" : "userInfo@tp.com",
                "MID" : "FbFRgc66424314189642CT",
                "MOBILE_NO" : userData['details']['phone'],
                "ORDERID" : trncID,
                "ORDER_ID" : trncID,
                "RESPCODE" : "141",
                "RESPMSG" : "Txn Conplete By Calling team",
                "STATUS" : "TXN_SUCCESS",
                "TXNAMOUNT" : amount,
                "TXNDATE" : datetime.now().strftime("%Y-%m-%d %H.%M.%S"),
                "TXNID" : "20200623111212800110168559732604329CT",
                "TXN_AMOUNT" : amount,
                "cmnts" : "By Calling Team",
                "coupon" : False,
                "sp" : amount*6

            })
            try:
                wallet = userData['wallet']['balance']
            except:
                wallet = 0
            database.child('users').child(idd).child('wallet').update({
                'balance':str(int(wallet)+int(amount*6)),
                
            })
            database.child('users').child(idd).child('wallet').child('transactions').child(trncID).update({
                "BANKTXNID" : "",
                "CURRENCY" : "INR",
                "CUST_ID" : userData['details']['name']+"@"+idd,
                "EMAIL" : "userInfo@tp.com",
                "MID" : "FbFRgc66424314189642CT",
                "MOBILE_NO" : userData['details']['phone'],
                "ORDERID" : trncID,
                "ORDER_ID" : trncID,
                "RESPCODE" : "141",
                "RESPMSG" : "Txn Conplete By Calling team",
                "STATUS" : "TXN_SUCCESS",
                "TXNAMOUNT" : amount,
                "TXNDATE" : datetime.now().strftime("%Y-%m-%d %H.%M.%S"),
                "TXNID" : "20200623111212800110168559732604329CT",
                "TXN_AMOUNT" : amount,
                "cmnts" : "By Calling Team",
                "coupon" : False,
                "sp" : amount*6

            })
            return redirect('/user/viewStu')
        else:
            return render(request,'./users/addMoney.html',{'id':idd,'error':"Please enter amount"})
    return render(request,'./users/addMoney.html',{'id':idd})
