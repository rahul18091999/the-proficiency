from django.shortcuts import render
from exam.views import database
# Create your views here.

def viewTickets(request):
    ticket = database.child('tickets').get()
    l=[]
    for i in ticket:
        for j in i.val():
            print(j)
            if j != "free":
                l.append(
                    {
                        'UID': i.key(),
                        'TID': j,
                        'dnt': i.val()[j]['dNt'],
                        'status': i.val()[j]['status'],
                        'title': i.val()[j]['title']
                    }
                )
    return render(request, './tickets/viewTickets.html',{'data':l})
def seeTicket(request):
    return render(request,'./tickets/seeTicket.html')