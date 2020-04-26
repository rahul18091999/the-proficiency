from django.shortcuts import render
from exam.views import checkpermission,database
# Create your views here.


def editprofile(request):
    id = request.session['user']
    marketerdata = database.child('marketers').child(id).child('details').get()
    l=[]
    l.append(
        {
            'id': id,
            'name': marketerdata.val()["name"],
            'age':marketerdata.val()["age"],
            'city':marketerdata.val()["city"],
            'email':marketerdata.val()["email"],
            'experience':marketerdata.val()["experience"],
            'gen':marketerdata.val()["gen"],
            'phone':marketerdata.val()["phone"],
            'state':marketerdata.val()["state"],
        }
    )
    return print('l')


def referral(request):
    idd=request.session['user']
    data=database.child('share').child('marketers').child(idd).get()
    totalearning = data.val()['earned']
    typea=data.val()['typeA']
    typeb=data.val()['typeB']    
    typec=data.val()['typeC']
    code={'typea':typea['code'],'typeb':typeb['code'],'typec':typec['code']}
    typeatrnc=[]
    typebtrnc=[]
    typectrnc=[]
    if 'trnc' in typea:
        for i in typea['trnc']:
            typeatrnc.append({'trnc':i,'earn':typea['trnc'][i]})
    if 'trnc' in typeb:
        for i in typeb['trnc']:
            typebtrnc.append({'trnc':i,'earn':typeb['trnc'][i]})
    if 'trnc' in typec:
        for i in typec['trnc']:
            typectrnc.append({'trnc':i,'earn':typec['trnc'][i]})
    return render(request,'./marketer/referal.html',{'code':code,'typeatrnc':typeatrnc,'typebtrnc':typebtrnc,'typectrnc':typectrnc})
