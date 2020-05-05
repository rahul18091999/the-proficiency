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