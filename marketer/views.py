from django.shortcuts import render,redirect
from exam.views import checkpermission, database,getpass
# Create your views here.


def editprofile(request):
    idd = request.session['user']
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
                    return redirect('/marketer/editProfile')

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
                        return redirect('/marketer/editProfile')
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


def referal(request):
    idd = request.session['user']
    data = database.child('share').child('marketers').child(idd).get()
    totalearning = data.val()['earned']
    typea = data.val()['typeA']
    typeb = data.val()['typeB']
    typec = data.val()['typeC']
    code = {'typea': typea['code'],
            'typeb': typeb['code'], 'typec': typec['code']}
    typeatrnc = []
    typebtrnc = []
    typectrnc = []
    if 'trnc' in typea:
        for i in typea['trnc']:
            typeatrnc.append({'trnc': i, 'earn': typea['trnc'][i]})
    if 'trnc' in typeb:
        for i in typeb['trnc']:
            typebtrnc.append({'trnc': i, 'earn': typeb['trnc'][i]})
    if 'trnc' in typec:
        for i in typec['trnc']:
            typectrnc.append({'trnc': i, 'earn': typec['trnc'][i]})
    return render(request, './marketer/referal.html', {'code': code, 'typeatrnc': typeatrnc, 'typebtrnc': typebtrnc, 'typectrnc': typectrnc})
