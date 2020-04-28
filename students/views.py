from django.shortcuts import render
from exam.views import database
# Create your views here.

def cmpp(x,y):
    return x-y

def analysis(request):
    d=database.child('/').get()
    NLEdate=list(d.val()['exams']['NLE'].keys())
    for i in range(len(NLEdate)):
        NLEdate[i]=NLEdate[i][4:]+'-'+NLEdate[i][2:4]+'-'+NLEdate[i][:2]
    NLEdate.sort()
    dailyTimedate=list(d.val()['exams']['dailyTime'].keys())
    for i in range(len(dailyTimedate)):
        dailyTimedate[i]=dailyTimedate[i][4:]+'-'+dailyTimedate[i][2:4]+'-'+dailyTimedate[i][:2]
    dailyTimedate.sort()

    if request.method == "POST":
        exam=request.POST.get('exam')
        date = request.POST.get('date')
        if date:
            if exam == 'Daily Exam':
                mainly=[]
                ud=[]
                tim=[]
                arrMarks = []
                income = []
                tID = []
                resp=d.val()
                for user in resp['users']:
                    topicID=[]
                    topics=[]
                    
                    if 'exams' in resp['users'][user] and 'daily' in resp['users'][user]['exams'] and date in resp['users'][user]['exams']['daily']:
                        ans=resp['users'][user]['exams']['daily'][date]['answers']
                        marks = 0
                        for q in range(1,len(ans)):
                            if ("opt"+str(ans[q]['selected']) == resp['questions'][ans[q]['qID']]['details']['optC']):
                                marks+=4
                                if ans[q]['topicID'] not in topicID:
                                    topicID.append(ans[q]['topicID'])
                                    topics.append(0);
                                topics[topicID.index(ans[q]['topicID'])]+=1
                                firebase
                                database.child('users').child(user).child('exams').child('daily').child(date).child('answers').child(q).update({
                                    'isCorrect' : 'true'
                                })
                            else:
                                marks-=1
                                firebase
                                database.child('users').child(user).child('exams').child('daily').child(date).child('answers').child(q).update({
                                    'isCorrect' : 'false',
                                    'correct' : resp['questions'][ans[q]['qID']]['details']['optC']
                                })

                            if ans[q]['by'] not in tID:
                                tID.append(ans[q]['by'])
                                income.append(0)
                            income[tID.index(ans[q]['by'])]+=1
                        for index,item in enumerate(topicID):
                            database.child('users').child(user).child('exams').child('analysis').child('topics').child(item).update({
                                'correct':topics[index]
                            })
                        if resp['users'][user]['prepFor']['mainly'] not in mainly:
                            mainly.append(resp['users'][user]['prepFor']['mainly'])
                            arrMarks.append([])
                        arrMarks[mainly.index(resp['users'][user]['prepFor']['mainly'])].append({
                            'marks':marks,
                            
                            'name':resp['users'][user]['details']['name'],
                            'uID':user,
                        })
                
                from operator import itemgetter
                for m in range(len(arrMarks)):
                    arrMarks[m].sort(key=itemgetter('marks'),reverse=True)
                    for u in range(len(arrMarks[m])):
                        percentile= round((100*(u+1)/len(arrMarks[m])),6)
                        rank = (((100 - percentile)/100)*len(arrMarks))+1
                        database.child('users').child(arrMarks[m][u]['uID']).child('exams').child('daily').child(date).update({
                            'marks':arrMarks[m][u]['marks'],
                            'percentile':percentile,
                            'rank':rank
                        })
                for index,item in enumerate(tID):
                    database.child('teachers').child(item).child('income').child('exams').child('daily').child(date).update({
                        'totalSale':income[index]
                    })
                'success':'Data has been analyzed Successfully.'
                        
            return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'success':success})
        else:
            error="Please Select all the details."
            return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'error':error})
    return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate})