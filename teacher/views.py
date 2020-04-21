from django.shortcuts import render
import re

from exam.views import database, getpass
# Create your views here.


def teacher(request):
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
        if (database.child('tIds').child(number).shallow().get().val()):
            error = "Phone Number Already exists"
            data['error'] = error
            return render(request, 'teacher.html', data)
        else:
            if userType == "Teacher":
                free = database.child('tIds').child(
                    'free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 100001
                from datetime import datetime
                from random import randint

                time_now = int(datetime.now().timestamp()*100)
                # print(time_now)
                database.child('tIds').child("12"+str(tempid)).update({
                    'createdOn': time_now,
                    'id': "12"+str(tempid),
                    'verify': randint(100000, 999999),
                    'pass': getpass(number+"@TP@"+age)[2:-1]
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
                free = database.child('aIds').child(
                    'free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 1000
                from datetime import datetime
                from random import randint

                time_now = int(datetime.now().timestamp()*100)
                create = request.session['user']
                database.child('aIds').child("13"+str(tempid)).update(
                    {
                        'createdOn': time_now,
                        'createdby': create,
                        'pass': getpass(number+"@TP@"+age)[2:-1]
                    }
                )
                database.child('admin').child('13'+str(tempid)).child('details').update(
                    {
                        'name': name,
                        'phoneNo':number,
                    }
                )
                database.child('aids').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',

                }
                data['success'] = "Admin has been added Successfully!"
                data['info'] = number + "@AP@" + age + " and 12" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, 'teacher.html', data)
                
            elif userType == 'Typer':
                free = database.child('tyIds').child(
                    'free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 100000
                from datetime import datetime
                from random import randint

                time_now = int(datetime.now().timestamp()*100)
                create = request.session['user']
                database.child('tyIds').child("14"+str(tempid)).update(
                    {
                        'createdOn': time_now,
                        'createdby': create,
                        'pass': getpass(number+"@TP@"+age)[2:-1]
                    }
                )
                database.child('typers').child('14'+str(tempid)).child('details').update(
                    {
                        'name': name,
                        'phoneNo':number,
                    }
                )
                database.child('tyIds').update({'free': tempid+1})
                data = {
                    'name': '',
                    'email': '',

                }
                data['success'] = "Typer has been added Successfully!"
                data['info'] = number + "@TYP@" + age + " and 12" + str(
                    tempid) + " is the Password and ID for " + ("Mr. " if gen == 'Male' else "Ms. ") + name
                return render(request, 'teacher.html', data)
            elif userType == "Marketer":
                data = {
                    'name': '',
                    'email': '',

                }
                data['success'] = "Marketer has been added Successfully!"
                data['info'] = number + "@MP@" + age + " and 12" + str(
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


def viewTeacher(request):
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
    # print(l)
    return render(request, 'viewTeacher.html', {'data': l})
