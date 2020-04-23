from django.shortcuts import render,redirect
from exam.views import checkpermission,database

def dashboard(request):
    print(request.GET.get('id'))
    return render(request,'dashboard.html')

def viewQues(request, ide):
    user = request.session['us']
    if ide == '1':
        if user == 14:
            iduser = request.session['user']
            typerdata = database.child('typers').child(iduser).child('questionsAdded').get()
            print(typerdata.val())
            l = []
            for i in typerdata:
                # id = i.val()['questionsAdded']['by']
                # if id == iduser:
                l.append(
                    {
                        'id': i.key(),
                        'by': iduser,
                    }
                )
            return render(request, 'viewQuestyper.html', {'question': l})
        else:
            typerdata = database.child('typers').child(ide).child('questionsAdded').get()
            print(typerdata.val())
            l = []
            for i in typerdata:
                # id = i.val()['questionsAdded']['by']
                # if id == iduser:
                l.append(
                    {
                        'id': i.key(),
                        'by': iduser,
                    }
                )
            return render(request, 'viewQuestyper.html', {'question': l})
    else:
        typerdata = database.child('typers').child(ide).child('questionsAdded').get()
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


# apiLogin/id=CryptedForm