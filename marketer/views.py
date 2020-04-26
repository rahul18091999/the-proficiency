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
        'id': id,
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
        if (currentpassword=="" and newpassword=="" and confirmpassword==""):
            return redirect("/home")
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
