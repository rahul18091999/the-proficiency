from django.shortcuts import render, redirect
from exam.views import checkpermission, database,storage,getpass
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
    typerdata = database.child('typers').child(iduser).child('questionsAdded').get()
    try:
        l = []
        for i in typerdata:
            l.append(
                {
                    'id': i.key(),
                    'by': i.val()["by"],
                }
            )
        return render(request, 'viewQuestyper.html', {'question': l})
    except:
        return render(request, 'viewQuestyper.html', {})


def editProfile(request):
    iduser = request.session['user']
    i = database.child('typers').child(iduser).child('details').get()
    from datetime import date
    data=database.child('tyIds').child(i.val()["phone"]).child('createdOn').get().val()/100
    date=date.fromtimestamp(data)
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
        'createdOn':date
    }
    if(request.method=="POST"):
        currentpassword=request.POST.get("currentpassword")
        newpassword=request.POST.get("newpassword")
        confirmpassword=request.POST.get("confirmpassword")
        if (currentpassword=="" and newpassword=="" and confirmpassword==""):
            return redirect("/home")
        else:
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './typer/editProfile.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('tyIds').child(i.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './typer/editProfile.html', {'data': l,'error':"Check Your Current Password"})
                else:
                    database.child('tyIds').child(i.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
                    return redirect('/home')


        
            # if (currentpassword=="" and newpassword=="" and confirmpassword==""):
            #     #add pic
            #     return
            # else:
            #     # add pic and pass
            #     if(newpassword!=confirmpassword or len(newpassword)<6):
            #         return render(request, './typer/editProfile.html', {'data': l,'error':"Check Your Password"})
            #     else:
            #         current=database.child('tyIds').child(i.val()["phone"]).child('pass').get().val()
            #         if(getpass(currentpassword)[2:-1]!=current):
            #             return render(request, './typer/editProfile.html', {'data': l,'error':"Check Your Current Password"})
            #         else:
            #             database.child('tyIds').child(i.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
            #             return redirect('/home')
             
        

        
        # storage.child('typers').child(request.session['user']).put(pic)
    else:
        
        return render(request, './typer/editProfile.html', {'data': l})
