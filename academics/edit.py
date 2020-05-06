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
        prep=request.POST.get('prepration')
        if (name != "" and dis != "" and prep is not None):
            print(prep)
            if prep == idprep:
                print("same")
                database.child('prepration').child(idprep).child('mainly').child(idd).child('details').update(
                    {
                        'name': name,
                        'dis': dis,
                    }
                )
                return redirect('/academics/viewMainly')
            else:
                print("diff")
                free = database.child('prepration').child(prep).child('mainly').child('free').shallow().get().val()
                if free:
                    tempid = free
                else:
                    tempid = 100
                database.child('prepration').child(prep).child('mainly').child(prep+str(tempid)).child('details').update(
                    {
                        'name': name,
                        'dis': dis,
                    }
                )
                database.child('prepration').child(prep).child('mainly').update({'free': tempid+1})
                data = {
                        'name': '',
                        'dis': '',
                    }
                database.child('prepration').child(idprep).child('mainly').child(idd).remove()
                return redirect('/academics/viewMainly')
    return render(request, './academics/editMainly.html',{'data':preprationdata,'main':l})