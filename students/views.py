from django.shortcuts import render,redirect
from exam.views import database,getpass
# Create your views here.

# def cmpp(x,y):
#     return x-y


# def panda(request):
#     d=database.child('/').get().val()
#     resp=d['users']
#     import pandas as pd
#     from pandas.io.json import json_normalize  
#     r=json_normalize(resp)
#     print(r)

#     print('hello')
#     return None




    
def forgotPassword(request):
    try:

        del request.session['step']
        del request.session['number']
    except:
        pass
    if request.method == 'POST':
        number = request.POST.get('number')
       
        data = list(database.child('ids').shallow().get().val())
       
        if number in data :
            import random
            from datetime import datetime
            ran = random.randint(100000,999999)
            
            database.child('ids').child(number).child('forgetPass').update({
                'code':ran,
                'time':int(datetime.now().timestamp()*1000)
            })
            import requests
            msgdata = database.child('sms').get().val()
            requests.get("http://sms.whybulksms.com/api/sendhttp.php?authkey="+msgdata['key']+"&mobiles="+number+"&message="+msgdata['msg']['forgetPass']+str(ran)+"&sender="+msgdata['sndrID']+"&route=4")
            request.session['step']=2
            request.session['number']=number
            return redirect('/students/newPassword')
        else:
            return render(request,'./students/forgotPassword.html',{'error':"Please fill correct number"})      
    return render(request,'./students/forgotPassword.html')

def newPassword(request):
        try:
            step = request.session['step']
            number = request.session['number']
            if step == 2:
                if request.method == 'POST':
                    code = request.POST.get('code')
                    c = database.child('ids').child(number).child('forgetPass').get().val()['code']
                    if str(c) == code:                        
                        request.session['step'] = 3                        
                        return render(request,'./students/newPassword.html')
                    else:
                        return render(request,'./students/verify.html',{'error':"Please fill correct code"})
                else:
                    return render(request,'./students/verify.html')           
            if step == 3:                
                if request.method == 'POST':
                    password = request.POST.get('pass')
                    conpassword = request.POST.get('conpass')                    
                    if (password ==conpassword and len(password)>=6):                       
                        database.child('ids').child(number).update({'pass':getpass(password)[2:-1]})
                        del request.session['step']
                        del request.session['number']
                        return render(request,'./students/forgotPassword.html',{'success':"Password change successfully."})
                    else:
                        return render(request,'./students/newPassword.html',{'error':'Password and confirm password must be equal nd minimun length must be greater than or equal to 6'}) 
                else:
                    return render(request,'./students/newPassword.html')
        except:
            return redirect('/students/forgetPassword')
       