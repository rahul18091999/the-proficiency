from django.shortcuts import render
from exam.views import database
# Create your views here.

def viewNotifications(request):
    d = database.child('notifications').get().val()
    l=[]
    if d:
        from datetime import datetime
        for i in d:
            if i !='free':
                l.append({
                    'nid':i,
                    'time':datetime.fromtimestamp(d[i]['time']/1000),
                    'title':d[i]['title'],
                    'to':d[i]['to']
                })
    return render(request,'./notification/viewNotifications.html',{'data':l})


def addNotifications(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('discription')
        to = request.POST.get('to')
        print(to)
        
        if(title and desc and to):
            data = database.child(to).get().val()
            token=[]
            td = data
            from datetime import datetime
            time_now = int(datetime.now().timestamp()*1000)
            print(time_now)
            tid = {}
            if data:
                temp = database.child('notifications').child('free').shallow().get().val()
                if temp:
                    idd = temp
                else:
                    idd = 100000000000000
                print(temp)
                for j in data:
                    tid[j] = 'done'
                    if 'notifications' in data[j]:
                        
                        if 'token' in data[j]['notifications']:
                        
                            token.append(data[j]['notifications']['token'])
                        

                    else:
                        td[j]['notifications']={}
                    if 'notes' not in data[j]['notifications']:
                        td[j]['notifications']['notes']={}
                    td[j]['notifications']['notes'][idd]=time_now

            if token:
                print(token)
                token.append('EfadsfadsfasdfasdxponentPushfasdTofsadfskfadssdafsdfen[4iSHToD76BENf7-ujv4hcN')
                import requests
                r = requests.post('https://exp.host/--/api/v2/push/send',
                headers={
                    "HTTP_ACCEPT":'application/json',
                    "HTTP_ACCEPT_ENCODING":'gzip, deflate',
                    "HTTP_HOST":'the-proficiency.com',
                    'Content-type': 'application/json'
                },
                json={
                    'to':token,                        
                      'title': title,                  
                      'body': desc,             
                      'priority': "high",            
                      'sound':"default",              
                      'channelId':"default",   

                })
                import ast
                d = ast.literal_eval(r.text)['data']
                if d[0]['status'] == 'ok':
                    database.child('notifications').child(idd).update({
                        'by':request.session['user'],
                        'discription':desc,
                        'time':time_now,
                        'title':title,
                        'to':to,
                        'ids':tid
                    })
                    database.child('notifications').update({'free':idd+1})
                    database.child('/').update({to:td})
        else:
            data={
                'title':title,
                'desc':desc,
                'to':to,
                'error':"Please fill all the details."
            }
            return render(request,'./notification/addNotifications.html',{'data':data})
    return render(request,'./notification/addNotifications.html')


def seeNotifications(request):
    nid = request.GET.get('nid')
    data = database.child('notifications').child(nid).get().val()
    from datetime import datetime
    data['time']= datetime.fromtimestamp(data['time']/100)
    return render(request,'./notification/seeNotifications.html',{'data':data, 'nID':nid})


    