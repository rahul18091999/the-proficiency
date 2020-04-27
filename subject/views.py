from django.shortcuts import render
from exam.views import database
from django.http import HttpResponse
# Create your views here.


def subject(request):
    return render(request, 'addSubject.html')


def viewsubjects(request):
    subjectdata = database.child('subjects').get()
    print(subjectdata)
    studentlist = []
    for i in subjectdata:
        if(i.key()!='free'):
            print(i.key)
            studentlist.append(
                {
                    'sId': i.key(),
                    'dis': i.val()['details']['dis'],
                    'name': i.val()['details']['name'],
                }
            )

    return render(request, 'viewSubjects.html',{'data': studentlist})


def addsubject(request):

    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        data = {
            'name': name,
            'dis': dis,
        }
        if (not name.replace('', '')):
            error = "please enter the name"
            data['error'] = error
            return render(request, 'addSubject.html', data)

        elif (not dis.replace('', '')):
            error = "please fill the discription"
            data['error'] = error
            return render(request, 'addSubject.html', data)
        else:
            free = database.child('subjects').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1001
            database.child('subjects').child("s"+str(tempid)).child('details').update(
                {
                    'dis': dis,
                    'name': name,
                }
            )
            data = {
                'name': '',
                'dis': '',
            }
            success = "subject added successfully"
            data['success'] = success
            database.child('subjects').update({'free': tempid+1})
            return render(request, 'addSubject.html', data)
    else:
        return HttpResponse("method not allowed")


