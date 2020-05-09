from django.shortcuts import render,redirect
from exam.views import database,getpass
# Create your views here.

# def cmpp(x,y):
#     return x-y

# def analysis(request):
#     d=database.child('/').get()
#     NLEdate=list(d.val()['exams']['NLE'].keys())
#     for i in range(len(NLEdate)):
#         NLEdate[i]=NLEdate[i][4:]+'-'+NLEdate[i][2:4]+'-'+NLEdate[i][:2]
#     NLEdate.sort()
#     dailyTimedate=list(d.val()['exams']['dailyTime'].keys())
#     for i in range(len(dailyTimedate)):
#         dailyTimedate[i]=dailyTimedate[i][4:]+'-'+dailyTimedate[i][2:4]+'-'+dailyTimedate[i][:2]
#     dailyTimedate.sort()
#     if request.method == "POST":
#         exam=request.POST.get('exam')
#         date = request.POST.get('date')

#         if date:
#             if exam == 'Daily Exam':
#                 mainly=[]
#                 ud=[]
#                 tim=[]
#                 arrMarks = []
#                 income = []
#                 tID = []
#                 resp=d.val()
#                 udata = resp['users']
#                 tdata = resp['teachers']
#                 for user in resp['users']:
#                     topicID=[]
#                     topics=[]
#                     if 'exams' in resp['users'][user] and 'daily' in resp['users'][user]['exams'] and date in resp['users'][user]['exams']['daily']:
#                         ans=resp['users'][user]['exams']['daily'][date]['answers']
#                         marks = 0
#                         for q in range(1,len(ans)):
#                             if ("opt"+str(ans[q]['selected']) == resp['questions'][ans[q]['qID']]['details']['optC']):
#                                 marks+=4
#                                 if ans[q]['topicID'] not in topicID:
#                                     topicID.append(ans[q]['topicID'])
#                                     topics.append(0);
#                                 topics[topicID.index(ans[q]['topicID'])]+=1
#                                 udata[user]['exams']['daily'][date]['answers'][q]['isCorrect'] = 'true'
#                             else:
#                                 marks-=1
#                                 udata[user]['exams']['daily'][date]['answers'][q]['isCorrect'] = 'false'
#                                 udata[user]['exams']['daily'][date]['answers'][q]['correct'] = resp['questions'][ans[q]['qID']]['details']['optC']                            
#                             if ans[q]['by'] not in tID:
#                                 tID.append(ans[q]['by'])
#                                 income.append(0)
#                             income[tID.index(ans[q]['by'])]+=1
#                         if 'analysis' not in udata[user]['exams']:
#                             udata[user]['exams']['analysis'] ={}
#                             udata[user]['exams']['analysis']['topics']={}
#                         for index,item in enumerate(topicID):
#                             udata[user]['exams']['analysis']['topics'][item]={'correct' : topics[index]}
#                         if resp['users'][user]['prepFor']['mainly'] not in mainly:
#                             mainly.append(resp['users'][user]['prepFor']['mainly'])
#                             arrMarks.append([])
#                         arrMarks[mainly.index(resp['users'][user]['prepFor']['mainly'])].append({
#                             'marks':marks,
                            
#                             'name':resp['users'][user]['details']['name'],
#                             'uID':user,
#                         })
#                 from operator import itemgetter
#                 for m in range(len(arrMarks)):
#                     s=sorted(arrMarks[m],key=itemgetter('name'),reverse=True)
#                     s=sorted(s, key=itemgetter('marks'))
#                     for u in range(len(s)):
#                         percentile= round((100*(u+1)/len(s)),6)
#                         rank = int(round((((100 - percentile)/100)*len(s))+1,0))
#                         udata[s[u]['uID']]['exams']['daily'][date]['marks']=s[u]['marks']
#                         udata[s[u]['uID']]['exams']['daily'][date]['percentile']=percentile
#                         udata[s[u]['uID']]['exams']['daily'][date]['rank']=rank

#                 for index,item in enumerate(tID):
#                     if 'income' not in tdata[item]:
#                         tdata[item]['income']={}
#                         tdata[item]['income']['exams']={}
#                         tdata[item]['income']['exams']['daily']={}
#                     tdata[item]['income']['exams']['daily'][date]={'totalSale':income[index]}

#                 success='Data has been analyzed Successfully.'                
                
#                 database.child('/').update({'users':udata,'teachers':tdata})
            
#             else:
#                 print(exam)
#                 mainly=[]
#                 ud=[]
#                 tim=[]
#                 arrMarks = []
#                 income = []
#                 tID = []
#                 resp=d.val()
#                 for user in resp['users']:
                    
#                     if 'exams' in resp['users'][user] and 'NLE' in resp['users'][user]['exams'] and date in resp['users'][user]['exams']['NLE']:
#                         ans=resp['users'][user]['exams']['NLE'][date]['answers']
                      
#                         marks = 0
#                         prep=resp['users'][user]['prepFor']['mainly']
                        
#                         for q in range(len(ans)):
                           
#                             idd=ans[q]['id']
                            
#                             if ("opt"+str(ans[q]['selected']) == resp['exams']['NLE'][date]['mainly'][prep]['questions'][str(idd)]['optC']):
#                                 marks+=4
#                                 database.child('users').child(user).child('exams').child('NLE').child(date).child('answers').child(q).update({
#                                     'isCorrect' : 'true'
#                                 })
#                             else:
#                                 print('NO')
#                                 marks-=1
#                                 # firebase
#                                 database.child('users').child(user).child('exams').child('NLE').child(date).child('answers').child(q).update({
#                                     'isCorrect' : 'false',
#                                     'correct' : resp['exams']['NLE'][date]['mainly'][prep]['questions'][str(idd)]['optC']
#                                 })
         
#                         if resp['users'][user]['prepFor']['mainly'] not in mainly:
#                             mainly.append(resp['users'][user]['prepFor']['mainly'])
#                             arrMarks.append([])
#                         arrMarks[mainly.index(resp['users'][user]['prepFor']['mainly'])].append({
#                             'marks':marks,
                            
#                             'name':resp['users'][user]['details']['name'],
#                             'uID':user,
#                         })
                
#                 from operator import itemgetter
#                 for m in range(len(arrMarks)):
#                     s=sorted(arrMarks[m],key=itemgetter('name'))
#                     s=sorted(s, key=itemgetter('marks'),reverse=True)
#                     for u in range(len(s)):
#                         percentile= round((100*(u+1)/len(s)),6)
#                         rank = (((100 - percentile)/100)*len(s))+1
                        
#                         database.child('users').child(s[u]['uID']).child('exams').child('NLE').child(date).update({
#                             'marks':s[u]['marks'],
#                             'percentile':percentile,
#                             'rank':rank
#                         })
#                 success='Data has been analyzed Successfully.'
#                 database.child('exams').child('NLE').child(date).update({'status':"Pre-Analysis Done"})

#             return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'success':success})
#         else:
#             error="Please Select all the details."
#             return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'error':error})
#     return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate})



# def overall(request):
#     aPID=[]
#     aP=[]
#     resp = database.child("/").get().val()
#     for user in resp['users']:
#         totalPercentile = 0
#         avgPercentile = 0
#         t = 0
#         if 'exams' in resp['users'][user]:
#             if 'daily' in resp['users'][user]['exams']:
#                 for dats in resp['users'][user]['exams']['daily']:
#                     if 'percentile' in resp['users'][user]['exams']['daily'][dats]:
#                         totalPercentile+=float(resp['users'][user]['exams']['daily'][dats]['percentile'])
#                         t+=1
#             if 'NLE' in resp['users'][user]['exams']:
#                 for dats in resp['users'][user]['exams']['NLE']:
#                     if 'percentile' in resp['users'][user]['exams']['NLE'][dats]:
#                         totalPercentile+=float(resp['users'][user]['exams']['NLE'][dats]['percentile'])
#                         t+=1
#             avgPercentile = round((totalPercentile/t),6)
#             if (resp['users'][user]['prepFor']['mainly'] not in aPID):
#                 aPID.append(resp['users'][user]['prepFor']['mainly'])
#                 aP.append([])
#             aP[aPID.index(resp['users'][user]['prepFor']['mainly'])].append({
#                 'uID': user,
#                 'mainly': resp['users'][user]['prepFor']['mainly'],
#                 'avgPercentile': avgPercentile,
#                 'name':resp['users'][user]['details']['name']
#             })
    
#     from operator import itemgetter
#     for m in range(len(aPID)):
#         s=sorted(aP[m],key=itemgetter('name'),reverse=True)
#         s=sorted(s,key=itemgetter('avgPercentile'))
#         print(s)
#         for a in range(len(s)):
#             percentile = round((100*(a+1)/len(s)),6)
#             rank = int(round((100-percentile)/100*len(s)+1,0))
#             print(percentile,rank)
#             database.child('ranks').child('students').child(s[a]['mainly']).child(s[a]['uID']).update({
#                 'rank':rank,
#                 'percentile':percentile,
#                 'name':s[a]['name']
#             })
#     return redirect


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
       