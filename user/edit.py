from django.shortcuts import render,redirect
from exam.views import database,checkpermission,getpass

def editteacher(request):
    iduser = request.GET.get('id')
    i = database.child('teachers').child(iduser).child('details').get()
    from datetime import date
    data=database.child('tIds').child(i.val()["phone"]).child('createdOn').get().val()/1000
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
        name = request.POST.get('name')
        number = request.POST.get('number')
        mail = request.POST.get('email')
        sate = request.POST.get('state')
        city = request.POST.get('city')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        if (currentpassword!="" and newpassword!="" and confirmpassword!=""):
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './users/editTeacher.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('tIds').child(i.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './users/editeditTeacher.html', {'data': l,'error':"Check Your Current Password"})
                else:
                    database.child('tIds').child(i.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
                    return redirect('/home')
        else:
            if (number == i.val()["phone"]):
                print(i.val()['phone'])
                database.child('teachers').child(iduser).child('details').update(
                    {
                        'name': name,
                        'age':age,
                        'city':city,
                        'email':mail,
                        'experience': experience,
                        'gen':i.val()["gen"],
                        'phone':i.val()["phone"],
                        'state':sate,
                    }
                )
                return redirect('/user/editteacher')

            else:
                if (database.child('tIds').child(number).shallow().get().val()):
                    error = "Phone Number Already exists"
                    data['error'] = error
                    return render(request, './users/editTeacher.html', data)
                else:
                    from random import  randint
                    database.child('tIds').child(number).update({
                        'createdOn': data,
                        'id': iduser,
                        'verify': randint(100000, 999999),
                        'pass': getpass(number+"@TP@"+age)[2:-1],
                        # 'createdBy': database.child('tIds').child(i.val()["phone"]).child('createdBy').get().val(),
                    })
                    database.child('tIds').child(i.val()['phone']).remove()
                    database.child('teachers').child(iduser).child('details').update(
                        {
                            'name': name,
                            'age': age,
                            'state': sate,
                            'city': city,
                            'experience': experience,
                            'phone': number,
                            'email': mail,
                            'gen': i.val()["gen"]
                        }
                    )
                    return redirect('/user/editteacher')
    else:
        
        return render(request, './users/editTeacher.html', {'data': l})


def editMarketer(request):
    idd = request.GET.get('id')
    print(idd)
    marketerdata = database.child('marketers').child(idd).child('details').get()
    print("marketerdata")
    from datetime import date
    data=database.child('mIds').child(marketerdata.val()["phone"]).child('createdOn').get().val()/1000
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
                    print("abc")
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
                    return redirect('/user/editmarketer?id='+idd)

                else:
                    if (database.child('mIds').child(number).shallow().get().val()):
                        error = "Phone Number Already exists"
                        data['error'] = error
                        return render(request, './users/editMarketer.html', data)
                    else:
                        from random import  randint
                        da=database.child('mIds').child(marketerdata.val()["phone"]).child('createdBY').get().val()
                        database.child('mIds').child(number).update({
                            'createdOn': data,
                            'id': idd,
                            'verify': randint(100000, 999999),
                            'pass': getpass(number+"@TP@"+age)[2:-1],
                            'createdBy': da,
                        })
                        database.child('mIds').child(marketerdata.val()['phone']).remove()
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
                        return redirect('/user/editmarketer')
        else:
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './users/editMarketer.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('mIds').child(marketerdata.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './users/editMarketer.html', {'data': l,'error':"Check Your Current Password"})
                else:
                    database.child('mIds').child(marketerdata.val()["phone"]).update({'pass':getpass(newpassword)[2:-1]})
                    return redirect('/home')
    else:
        return render(request, './users/editMarketer.html', {'data': l})

def edittyper(request):
    iduser = request.GET.get('id')
    print(iduser)
    i = database.child('typers').child(iduser).child('details').get()
    from datetime import date
    data=database.child('tyIds').child(i.val()["phone"]).child('createdOn').get().val()/1000
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
        name = request.POST.get('name')
        number = request.POST.get('number')
        mail = request.POST.get('email')
        sate = request.POST.get('state')
        city = request.POST.get('city')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        if (currentpassword=="" and newpassword=="" and confirmpassword==""):
                if (number == i.val()["phone"]):
                    print(i.val()['phone'])
                    database.child('typers').child(iduser).child('details').update(
                        {
                            'name': name,
                            'age':age,
                            'city':city,
                            'email':mail,
                            'experience': experience,
                            'gen':i.val()["gen"],
                            'phone':i.val()["phone"],
                            'state':sate,
                        }
                    )
                    return redirect('/user/edittyper')

                else:
                    if (database.child('tyIds').child(number).shallow().get().val()):
                        error = "Phone Number Already exists"
                        data['error'] = error
                        return render(request, './users/edittyper.html', data)
                    else:
                        from random import  randint
                        da=database.child('tyIds').child(i.val()["phone"]).child('createdBY').get().val()
                        database.child('tyIds').child(number).update({
                            'createdOn': data,
                            'id': iduser,
                            'verify': randint(100000, 999999),
                            'pass': getpass(number+"@TP@"+age)[2:-1],
                            'createdBy': da,
                        })
                        database.child('tyIds').child(i.val()['phone']).remove()
                        database.child('typers').child(iduser).child('details').update(
                            {
                                'name': name,
                                'age': age,
                                'state': sate,
                                'city': city,
                                'experience': experience,
                                'phone': number,
                                'email': mail,
                                'gen': i.val()["gen"]
                            }
                        )
                        return redirect('/user/edittyper')
        else:
            if(newpassword!=confirmpassword or len(newpassword)<6):
                return render(request, './users/edittyper.html', {'data': l,'error':"Check Your Password"})
            else:
                current=database.child('tyIds').child(i.val()["phone"]).child('pass').get().val()
                if(getpass(currentpassword)[2:-1]!=current):
                    return render(request, './users/edittyper.html', {'data': l,'error':"Check Your Current Password"})
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
        
        return render(request, './users/edittyper.html', {'data': l})
