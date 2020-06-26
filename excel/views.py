from django.shortcuts import render
import openpyxl
from exam.views import database,getpass,checkpermission
import urllib
# Create your views here.
def createAccount(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method=="POST":
        msg = request.POST.get("msg")
        if request.FILES and msg:
            file = request.FILES['file']        
            wb = openpyxl.load_workbook(file)
            msg = urllib.parse.quote(msg)
            import requests
            for cell in wb['Sheet1']:
                if str(cell[1].value):
                    requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey=13616AjiaVJD225eb53cc5P15&mobiles="+str(cell[1].value)+"&message="+msg+"&sender=PROCNC&route=4")
        else:
            return render(request,'./excel/createAccount.html',{'error':"Please check the details."})



        # data = database.child('/').get().val()
        
        # #free
        # if 'ids' not in data:
        #     data['ids']={}
        #     data['ids']['free']=100000

        # msgdata = database.child('sms').get().val()        
        # free = data['ids']['free']
        # from datetime import datetime
        # import urllib
        
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

    h = database.child('users').get().val()
    
    for i in h:
        if 'batch' in h[i]:
            if h[i]['batch']=='Weekend':
                h[i]['batch']='Weekdays'
            else:
                print(i)
        
    database.child('/').update({'users':h})
    print(h)