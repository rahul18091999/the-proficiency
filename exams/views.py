from django.shortcuts import render
from exam.views import database, checkpermission

# Create your views here.


def addNLEs(request):
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time !="":
            dat = date[8:]+date[5:7]+date[:4]
            print(dat)
            NLE = database.child('exams').child('NLE').child(dat)
            print("xyz")
            NLE.update(
                {
                    'time': time,
                }
            )
            print("time")
            data = database.child('prepration').get()
            if data.val():
                for i in data:
                    if (i.key() != 'free'):
                        if 'mainly' in i.val():
                            t = i.val()['mainly']
                            for j in t:
                                if j != 'free':
                                     database.child('exams').child('NLE').child(dat).child('mainly').child(j).update(
                                        {
                                            'name': t[j]['details']['name'],
                                            'dis': t[j]['details']['dis']
                                        }
                                    )
            print("abc")
            data = {
                'name': "",
                'dis': "",
            }
            success = "submitted successfully"
            data['success'] = success
            return render(request, './exams/addNLE.html', data)
        else:
            data = {
                'name': date,
                'dis': time,
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/addNLE.html', data)
    else:
        return render(request, './exams/addNLE.html')



def daily(request):
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time !="":
            dat = date[8:]+date[5:7]+date[:4]
            print(dat)
            NLE = database.child('exams').child('dailyTime').child(dat)
            print("xyz")
            NLE.update(
                {
                    'time': time,
                }
            )
            data = {
                'name': "",
                'dis': "",
            }
            success = "submitted successfully"
            data['success'] = success
            return render(request, './exams/addDaily.html', data)
        else:
            data = {
                'name': date,
                'dis': time,
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/addDaily.html', data)
    else:
        return render(request, './exams/addDaily.html')
