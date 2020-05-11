from django.shortcuts import render,redirect
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
    UID = request.GET.get('UID')
    TID = request.GET.get('TID')
    from datetime import datetime
    if UID and TID:
        ticket = database.child('tickets').child(UID).child(TID).get()
        l=[]
        ticketid={
            'TID': TID,
            'UID': UID,
            'dNt': ticket.val()['dNt'],
            'title': ticket.val()['title'],
            'dis': ticket.val()['dis'],
            'status': ticket.val()['status']
        }
        if 'replies' in ticket.val():
            replies = database.child('tickets').child(UID).child(TID).child('replies').get()
            for i in replies:
                l.append(
                    {   'userid': str(i.val()['by']),
                        'time': datetime.fromtimestamp(int(i.key())/100),
                        'reply': i.val()['reply']
                    }
                )
                # print(datetime.fromtimestamp(int(i.key())/1000))
                print(int(datetime.now().timestamp()*100))
        else:
            pass
        if request.method == "POST":
            print(datetime.now().timestamp()*1000)
            idd = request.session['user']
            msg = request.POST.get('message')
            time_now = int(datetime.now().timestamp()*1000)
            database.child('tickets').child(UID).child(TID).child('replies').child(time_now).update(
                {
                    'by': idd,
                    'reply': msg, 
                }
            )
            if ticket.val()['status']!="replied":
                database.child('tickets').child(UID).child(TID).update(
                    {
                        'dNt': ticket.val()['dNt'],
                        'dis': ticket.val()['dis'],
                        'status': 'replied',
                        'title': ticket.val()['title']

                    }

                )
            return redirect('/tickets/seeTicket?UID='+UID+"&TID="+TID)
        return render(request,'./tickets/seeTicket.html',{'mine':l,'ticketId':ticketid})

def changeStatus(request):
    UID = request.GET.get('UID')
    TID = request.GET.get('TID')
    status = request.POST.get('status')
    feed = request.POST.get('feed')
    if status and feed:
        ticket =  database.child('tickets').child(UID).child(TID).get()
        database.child('tickets').child(UID).child(TID).update(
                        {
                            'dNt': ticket.val()['dNt'],
                            'dis': ticket.val()['dis'],
                            'status': status,
                            'title': ticket.val()['title'],
                            'feedback': feed,

                        }

                    )
        return redirect('/tickets/seeTicket?UID='+UID+"&TID="+TID)
    else:
        return redirect('/tickets/seeTicket?UID='+UID+"&TID="+TID)
