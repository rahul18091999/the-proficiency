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