from django.shortcuts import render, redirect
from exam.views import checkpermission, database
from datetime import date

def dashboard(request):
    id = request.session['user']
    typersquestion = database.child('typers').child(
        id).child('questionsAdded').get()
    data = 0
    for i in typersquestion:
        data += 1
    return render(request, 'dashboard.html', {'data': data})


def viewQues(request):
    iduser = request.session['user']
    typerdata = database.child('typers').child(
        iduser).child('questionsAdded').get()
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


def editProfile(request):
    iduser = request.session['user']
    i = database.child('typers').child(iduser).child('details').get()
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
        'createdOn':database.child('tyIds').child(i.val()["phone"]).child('createdOn').get().val()
    }
    return render(request, './typer/editProfile.html', {'data': l})

def viewQues(request):
    iduser=request.session['user']
    typerdata = database.child('typers').child(iduser).child('questionsAdded').get()
    questions = database.child('questions').get()
    print(typerdata.val())
    l = []
    for i in typerdata:
        for j in questions:
            if j.key() == i.key() and j.key() != 'free':
                l.append(
                    {
                        'id': i.key(),
                        'approved': j.val()['details']['approved'],
                        'by': j.val()['details']['by']
                    }
                )
    return render(request, 'viewQuestyper.html', {'question': l})
