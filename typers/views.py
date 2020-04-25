from django.shortcuts import render, redirect
from exam.views import checkpermission, database


def dashboard(request):
<<<<<<< HEAD
    id = request.session['user']
    typersquestion = database.child('typers').child(id).child('questionsAdded').get()
=======
    idd = request.session['user']
    typersquestion = database.child('typers').child(idd).child('questionsAdded').get(
    )
>>>>>>> 84e3df2c0b68d4470f14bc3efc6758f401af4887
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