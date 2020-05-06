from django.shortcuts import render, redirect
from exam.views import database, checkpermission

def editBU(request):
    idd = request.GET.get('bid')
    BU = database.child('boards').child(idd).child('details').get()
    
    l=  {
            'id': idd,
            'name': BU.val()['name'],
            'dis': BU.val()['dis'],
        }
    
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('boards').child(idd).child('details').update(
            {
                'dis': dis,
                'name': name,
            }
        )
        return redirect('/academics/viewBU')
    else:
        return render(request,'./academics/editBU.html',{'data':l})


def editHD(request):
    idd = request.GET.get('hid')
    BU = database.child('hDegree').child(idd).child('details').get()
    l=  {
            'id': idd,
            'name': BU.val()['name'],
            'dis': BU.val()['dis'],
        }
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('hDegree').child(idd).child('details').update(
            {
                'dis': dis,
                'name': name,
            }
        )
        return redirect('/academics/viewHD')
    else:
        return render(request,'./academics/editHD.html',{'data':l})


def editMainly(request):
    idd = request.GET.get('id')
    prepdata=database.child('prepration').get()
    preprationdata=[]
    idprep = idd[:6]
    if prepdata.val():
        for i in prepdata:
            if i.key()!='free':
                preprationdata.append({'id':i.key(),'name':prepdata.val()[i.key()]['details']['name']})
    mainly=database.child('prepration').child(idprep).child('mainly').child(idd).child('details').get()
    prep = database.child('prepration').child(idprep).child('details').get()
    l=  {
            'id': idd,
            'name': mainly.val()['name'],
            'dis': mainly.val()['dis'],
            'prep':idprep,
            'prepname': prep.val()['name']

            }
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('prepration').child(idprep).child('mainly').child(idd).child('details').update(
            {
                'name': name,
                'dis': dis,
            }
        )
        return redirect('/academics/viewMainly')
    return render(request, './academics/editMainly.html',{'data':preprationdata,'main':l})







def editPrepFor(request):
    idd = request.GET.get('id')
    if request.method == "POST":
        print(idd)
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('prepration').child(idd).child('details').update(
            {
                'name': name,
                'dis': dis,
            }
        )
        return redirect('/academics/viewPrepFor')
    prepfor = database.child('prepration').child(idd).child('details').get()
    l={
        'name': prepfor.val()['name'],
        'dis': prepfor.val()['dis'],
        'id': idd,
    }
    return render(request,'./academics/editPrepFor.html',{'data':l})

def editTopic(request):
    idd = request.GET.get('id')
    sid = idd[:5]
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('subjects').child(sid).child('topics').child(idd).child('details').update(
            {
                'name': name,
                'dis': dis,
            }
        )
        return redirect('/academics/viewTopics')
    topics = database.child('subjects').child(sid).child('topics').child(idd).child('details').get()
    l={
        'name': topics.val()['name'],
        'dis': topics.val()['dis'],
        'id': idd,
    }
    return render(request,'./academics/editTopic.html',{'data':l})

def editSub(request):
    idd = request.GET.get('id')
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        database.child('subjects').child(idd).child('details').update(
            {
                'name': name,
                'dis': dis,
            }
        )
        return redirect('/academics/viewSubjects')
    topics = database.child('subjects').child(idd).child('details').get()
    l={
        'name': topics.val()['name'],
        'dis': topics.val()['dis'],
        'id': idd,
    }
    return render(request,'./academics/editSub.html',{'data':l})