from django.shortcuts import render, redirect
from exam.views import database, checkpermission, getpass
# Create your views here.
def getcode(typ):
    import random
    import string
    temp = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 3))
    if(typ=='a'):
        return temp
    elif(typ == 'b'):
        if(temp==typea):
            getcode('b')
        else:
            return temp 
    elif(typ=='c'):
        if(temp==typea or temp==typeb):
            getcode('c')
        else:
            return temp 

def dashboard(request):
    id = request.GET.get('id')
    typersquestion = database.child['typers'].child[id].child['questionsAdded'].get(
    )
    l = []
    for i in typersquestion:
        l.append(
            {
                'id': i.key(),
                'by': id,
            }
        )
    return render(request, 'viewQuestyper.html', {'question': l})


def users(request):
    global typea,typeb,typec
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    else:
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
            time_now = int(datetime.now().timestamp()*100)
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
                teachers = database.child('share').child('teachers').child('12'+str(tempid)).update(
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

                }
                data['success'] = "Teacher has been added Successfully!"
                data['info'] = number + "@TP@" + age + " and 12" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)
            elif userType == "Admin":
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
                        'pass': getpass(number+"@TP@"+age)[2:-1]
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
                database.child('aids').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',

                }
                data['success'] = "Admin has been added Successfully!"
                data['info'] = number + "@AP@" + age + " and 13" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
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

                }
                data['success'] = "Typer has been added Successfully!"
                data['info'] = number + "@TYP@" + age + " and 14" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)
            elif userType == "Marketer":
                if (database.child('MIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/addUser.html', data)
                free = database.child('mIds').child(
                    'free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 1000000

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

                }
                data['success'] = "Marketer has been added Successfully!"
                data['info'] = number + "@MP@" + age + " and 11" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, './users/addUser.html', data)
            
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
            print('1')
            return render(request, './users/addUser.html', data)


def viewteacher(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')   
    teacherData = database.child('teachers').get()
    # if teacherData:
    print(teacherData)
    l = []
    if(teacherData.val()):
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
            if(i.key()!='qBank'):
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
    l=[]
    if marketerData.val():
        for i in marketerData:
            print(i.key())
            l.append(
                {
                    'tId': i.key(),
                    'name': i.val()['details']['name'],
                    'number': i.val()['details']['phone'],
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
        adminQues = database.child['superAdmin'].child[id].child['questionsAdded'].get()
        l=[]
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
        adminQues = database.child['admin'].child[id].child['questionsAdded'].get()
        l=[]
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
    marketerdata = database.child('marketers').child(idd).child('details').get()
    from datetime import date
    data=database.child('mIds').child(marketerdata.val()["phone"]).child('createdOn').get().val()/100
    date=date.fromtimestamp(data)
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
        'createdOn':date
    }
    if(request.method=="POST"):
        currentpassword=request.POST.get("currentpassword")
        newpassword=request.POST.get("newpassword")
        confirmpassword=request.POST.get("confirmpassword")
        name = request.POST.get('name')
        number = request.POST.get('number')
        mail = request.POST.get('email')
        sate = request.POST.get('state')
        city = request.POST.get('city')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        if (currentpassword=="" and newpassword=="" and confirmpassword==""):
                if (number == marketerdata.val()["phone"]):
                    database.child('marketers').child(idd).child('details').update(
                        {
                            'name': name,
                            'age':age,
                            'city':city,
                            'email':mail,
                            'experience': experience,
                            'gen':marketerdata.val()["gen"],
                            'phone':marketerdata.val()["phone"],
                            'state':sate,
                        }
                    )
                    return redirect('/user/editMarketer')

                else:
                    if (database.child('mIds').child(number).shallow().get().val()):
                        error = "Phone Number Already exists"
                        data['error'] = error
                        return render(request, './marketer/editProfile.html', data)
                    else:
                        from random import  randint
                        da=database.child('mIds').child(marketerdata.val()["phone"]).child('createdBY').get().val()
                        database.child('mIds').child(number).update({
                            'createdOn': data,
                            'id': iduser,
                            'verify': randint(100000, 999999),
                            'pass': getpass(number+"@TP@"+age)[2:-1],
                            'createdBy': da,
                        })
                        database.child('mIds').child(marketerdata.val()['phone']).remove()
                        database.child('marketers').child(iduser).child('details').update(
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
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './marketer/editProfile.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('mIds').child(marketerdata.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './marketer/editProfile.html', {'data': l,'error':"Check Your Current Password"})
                else:
                    database.child('mIds').child(marketerdata.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
                    return redirect('/home')
    else:
        return render(request, './marketer/editProfile.html', {'data': l})

