from django.shortcuts import render
from exam.views import database
# Create your views here.
def addMsg(request):
    data = database.child('/').get().val()
    teacherdata = []
    if 'teachers' in data:
        for i in data['teachers']:
            if i!='qBank':
                teacherdata.append({'id':i,'name':data['teachers'][i]['details']['name']})
    marketerdata = []
    if 'marketers' in data:
        for i in data['marketers']:
                teacherdata.append({'id':i,'name':data['marketers'][i]['details']['name']})
    typerdata = []
    if 'typers' in data:
        for i in data['typers']:
                teacherdata.append({'id':i,'name':data['typers'][i]['details']['name']})
    if request.method=='POST':
        to = request.POST.get('to')
        select = request.POST.get('select')
        discription = request.POST.get('discription')
        if to and select  and discription:
            toData = database.child(to).get().val()
            if toData:
                td = toData
                from datetime import datetime
                time_now = int(datetime.now().timestamp()*1000)
                tid={}
                temp = database.child('msg').child('free').shallow().get().val()
                if temp:
                    idd = temp
                else:
                    idd = 100000000000000
                if select =='all':    
                    for j in toData:
                        tid[j] = 'done'
                        if 'msg' not in toData[j]:
                            td[j]['msg']={}
                        if 'notes' not in toData[j]['msg']:
                            td[j]['msg']['notes']={}
                        td[j]['msg']['notes'][idd]=time_now
                else:
                    
                    j=select
                    
                    tid[j] = 'done'
                    if 'msg' not in toData[j]:
                        td[j]['msg']={}
                    if 'notes' not in toData[j]['msg']:
                        td[j]['msg']['notes']={}
                    print(type(td[j]['msg']['notes']))
                    td[j]['msg']['notes'][idd]=time_now
                database.child('/').update({to:td})
                database.child('msg').child(idd).update({
                        'by':request.session['user'],
                        'discription':discription,
                        'time':time_now,
                        'to':to,
                        'ids':tid
                    })
                database.child('msg').update({'free':idd+1})
                    

                    
                
    return render(request,'./msg/addMsg.html',{'teacherdata':teacherdata,'marketerdata':marketerdata,'typerdata':typerdata})