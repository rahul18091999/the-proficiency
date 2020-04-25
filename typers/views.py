from django.shortcuts import render, redirect
from exam.views import checkpermission, database


def dashboard(request):
    id = request.session['user']
    typersquestion = database.child('typers').child(id).child('questionsAdded').get()
    data = 0
    for i in typersquestion:
        data += 1
    return render(request, 'dashboard.html', {'data': data})


def viewQues(request, ide):
    iduser = request.session['user']
    typerdata = database.child('typers').child(iduser).child('questionsAdded').get()
    print(typerdata.val())
    l = []
    for i in typerdata:
        l.append(
            {
                'id': i.key(),
                'by': iduser,
            }
        )
    return render(request, 'viewQuestyper.html', {'question': l})