from django.shortcuts import render
import openpyxl
from exam.views import database,getpass
# Create your views here.
def createAccount(request):
    if request.method=="POST":
        file = request.FILES['file']

        # file = open(file,'rb')
        
        wb = openpyxl.load_workbook(file)
        # data = database.child('/').get().val()
        
        # #free
        # if 'ids' not in data:
        #     data['ids']={}
        #     data['ids']['free']=100000

        # msgdata = database.child('sms').get().val()        
        # free = data['ids']['free']
        # from datetime import datetime
        # import urllib
        import requests
        for cell in wb['Sheet1']:
            requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey=13616AjiaVJD225eb53cc5P15&mobiles="+str(cell[0].value)+"&message=Quiz%20has%20been%20started.%20All%20the%20Best%5CnTeam%20ThePROFICIENCY&sender=PROCNC&route=4")
        # time_now = int(datetime.now().timestamp()*1000)
        # for cell in wb["Sheet1"]:
        #     data['users']['20'+str(free)]={}
        #     data['users']['20'+str(free)]['details']={
        #         'name':cell[0].value,
        #         'parent':'XXXXXXXXXX',
        #         'phone':cell[1].value,
        #     }
        #     data['ids'][cell[1].value]={
        #         'code':"",
        #         'createdOn':time_now,
        #         'id':'20'+str(free),
        #         'im':"s",
        #         'once':"",
        #         'pass':str(getpass(cell[3].value)[2:-1]),
        #         'verify':cell[4].value,
        #     }

        #     free+=1
            # requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey="+msgdata['key']+"&mobiles="+str(cell[1].value)+"&message="+urllib.parse.quote(msgdata['msg']['verification']+str(cell[4].value))+"&sender="+msgdata['sndrID']+"&route=4")
        # data['ids']['free']=free
        # database.child('/').update(data)       
        
    return render(request,'./excel/createAccount.html')


def send(request):
#     msg=urllib.parse.quote("Dear Student, as you've filled our form for 
# For more info call:- +917072191877, +918810544042, +917424959601, +918307264602, +918295848645")
    h = database.child('users').get().val()
    print(h)
    for i in h:
        h[i]['details']['phone']=str(h[i]['details']['phone'])
    database.child('/').update({'users':h})
    print(h)