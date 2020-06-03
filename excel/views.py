# from django.shortcuts import render
# import openpyxl
# from exam.views import database,getpass
# # Create your views here.
# def createAccount(request):
#     if request.method=="POST":
#         file = request.FILES['file']

#         # file = open(file,'rb')
        
#         # wb = openpyxl.load_workbook(file)
#         # data = database.child('/').get().val()
        
#         # #free
#         # if 'ids' not in data:
#         #     data['ids']={}
#         #     data['ids']['free']=100000

#         # msgdata = database.child('sms').get().val()        
#         # free = data['ids']['free']
#         # from datetime import datetime
#         # import urllib
#         # import requests
#         # for cell in wb['Sheet1']:
#         #     requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey=13616AjiaVJD225eb53cc5P15&mobiles="+str(cell[1].value)+"&message=Dear%20Student%2C%20as%20you've%20filled%20our%20form%20for%20the%20Quiz%2C%20Quiz%20is%20going%20to%20be%20start%20sharp%20at%207%20P.M.%20and%20to%20download%20the%20App%20Tap%20the%20Link%20below%3A-%20https%3A%2F%2Fbit.ly%2FThePROCNC030620%20Username%20%3D%20"+str(cell[1].value)+"%20Password%20%3D%20"+cell[3].value+"%20For%20more%20info%20call%3A-%20%2B917072191877%2C%20%2B918810544042%2C%20%2B917424959601%2C%20%2B918307264602%2C%20%2B918295848645&sender=PROCNC&route=4")
#         # time_now = int(datetime.now().timestamp()*1000)
#         # for cell in wb["Sheet1"]:
#         #     data['users']['20'+str(free)]={}
#         #     data['users']['20'+str(free)]['details']={
#         #         'name':cell[0].value,
#         #         'parent':'XXXXXXXXXX',
#         #         'phone':cell[1].value,
#         #     }
#         #     data['ids'][cell[1].value]={
#         #         'code':"",
#         #         'createdOn':time_now,
#         #         'id':'20'+str(free),
#         #         'im':"s",
#         #         'once':"",
#         #         'pass':str(getpass(cell[3].value)[2:-1]),
#         #         'verify':cell[4].value,
#         #     }

#         #     free+=1
#             # requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey="+msgdata['key']+"&mobiles="+str(cell[1].value)+"&message="+urllib.parse.quote(msgdata['msg']['verification']+str(cell[4].value))+"&sender="+msgdata['sndrID']+"&route=4")
#         # data['ids']['free']=free
#         # database.child('/').update(data)       
        
#     return render(request,'./excel/createAccount.html')


# def send(request):
# #     msg=urllib.parse.quote("Dear Student, as you've filled our form for 
# # For more info call:- +917072191877, +918810544042, +917424959601, +918307264602, +918295848645")
#     h = database.child('users').get().val()
#     print(h)
#     for i in h:
#         h[i]['details']['phone']=str(h[i]['details']['phone'])
#     database.child('/').update({'users':h})
#     print(h)