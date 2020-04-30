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
    print(database.child('questions').child('q1000000001').get().val())
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
                                # firebase
                                database.child('users').child(user).child('exams').child('daily').child(date).child('answers').child(q).update({
                                    'isCorrect' : 'true'
                                })
                            else:
                                marks-=1
                                # firebase
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
                print(arrMarks)
                from operator import itemgetter
                for m in range(len(arrMarks)):
                    s=sorted(arrMarks[m],key=itemgetter('name'),reverse=True)
                    s=sorted(s, key=itemgetter('marks'))
                    print(s)
                    for u in range(len(s)):
                        percentile= round((100*(u+1)/len(s)),6)
                        rank = int(round((((100 - percentile)/100)*len(s))+1,0))
                        print(percentile,rank,s[u]['uID'])
                        database.child('users').child(s[u]['uID']).child('exams').child('daily').child(date).update({
                            'marks':s[u]['marks'],
                            'percentile':percentile,
                            'rank':rank
                        })
                for index,item in enumerate(tID):
                    database.child('teachers').child(item).child('income').child('exams').child('daily').child(date).update({
                        'totalSale':income[index]
                    })
                success='Data has been analyzed Successfully.'
                database.child('exams').child('dailyTime').child(date).update({'status':"Pre-Analysis Done"})
            else:
                print(exam)
                mainly=[]
                ud=[]
                tim=[]
                arrMarks = []
                income = []
                tID = []
                resp=d.val()
                for user in resp['users']:
                    
                    if 'exams' in resp['users'][user] and 'NLE' in resp['users'][user]['exams'] and date in resp['users'][user]['exams']['NLE']:
                        ans=resp['users'][user]['exams']['NLE'][date]['answers']
                      
                        marks = 0
                        prep=resp['users'][user]['prepFor']['mainly']
                        
                        for q in range(len(ans)):
                           
                            idd=ans[q]['id']
                            
                            if ("opt"+str(ans[q]['selected']) == resp['exams']['NLE'][date]['mainly'][prep]['questions'][str(idd)]['optC']):
                                marks+=4
                                database.child('users').child(user).child('exams').child('NLE').child(date).child('answers').child(q).update({
                                    'isCorrect' : 'true'
                                })
                            else:
                                print('NO')
                                marks-=1
                                # firebase
                                database.child('users').child(user).child('exams').child('NLE').child(date).child('answers').child(q).update({
                                    'isCorrect' : 'false',
                                    'correct' : resp['exams']['NLE'][date]['mainly'][prep]['questions'][str(idd)]['optC']
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
                    s=sorted(arrMarks[m],key=itemgetter('name'))
                    s=sorted(s, key=itemgetter('marks'),reverse=True)
                    for u in range(len(s)):
                        percentile= round((100*(u+1)/len(s)),6)
                        rank = (((100 - percentile)/100)*len(s))+1
                        
                        database.child('users').child(s[u]['uID']).child('exams').child('NLE').child(date).update({
                            'marks':s[u]['marks'],
                            'percentile':percentile,
                            'rank':rank
                        })
                success='Data has been analyzed Successfully.'
                database.child('exams').child('NLE').child(date).update({'status':"Pre-Analysis Done"})

            return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'success':success})
        else:
            error="Please Select all the details."
            return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate,'error':error})
    return render(request,'./students/viewAnalysis.html',{'NLE':NLEdate,'daily':dailyTimedate})



def overall(request):
    aPID=[]
    ap=[]
    resp = database.child("/").get().val()
    for user in resp['users']:
        print(user)
        totalPercentile = 0
        avgPercentile = 0
        t = 0
        if 'exams' in resp['users'][user]:
            if 'daily' in resp['users'][user]['exams']:
                for dats in resp['users'][user]['exams']['daily']:
                    # if
                    totalPercentile+=float(resp['users'][user]['exams']['daily'][dats]['percentile'])
                    t+=1
            if 'NLE' in resp['users'][user]['exams']:
                for dats in resp['users'][user]['exams']['NLE']:
                    totalPercentile+=float(resp['users'][user]['exams']['NLE'][dats]['percentile'])
                    t+=1
            avgPercentile = round((totalPercentile/t)*100,6)

#     module.exports = (req, res, next) => {
#     var aPID = [];
#     var aP = [];
#     fire.ref("/").once('value', (response) => {
#         const resp = response.val()
#         for (var user in resp.users) {
#             var totalPercentile = 0;
#             var avgPercentile = 0;
#             var t = 0;
#             if (typeof (resp.users[`${user}`].exams) != 'undefined' && typeof (resp.users[`${user}`].exams.daily) != 'undefined') {
#                 for (var dats in resp.users[`${user}`].exams.daily) {
#                     totalPercentile += resp.users[`${user}`].exams.daily[`${dats}`].percentile
#                     t += 1;
#                 }
#                 avgPercentile = ((totalPercentile / t) * 100).toFixed(6);
#                 if (aPID.indexOf(resp.users[`${user}`].prepFor.prepFor) == -1) {
#                     aPID.push(resp.users[`${user}`].prepFor.prepFor)
#                     aP.push([])
#                 }
#                 aP[aPID.indexOf(resp.users[`${user}`].prepFor.prepFor)].push({
#                     uID: user,
#                     mainly: resp.users[`${user}`].prepFor.prepFor,
#                     avgPercentile: avgPercentile,
#                 })
#             }
#         }
#         for (var m = 0; m < aPID.length; m++) {
#             aP[m].sort(function (a, b) { return a.avgPercentile - b.avgPercentile });
#             for (var a = 0; a < aP[m].length; a++) {
#                 var percentile = (100 * (a + 1) / aP[m].length).toFixed(6);
#                 var rank = Math.round((((100 - percentile) / 100) * aP[m].length) + 1);
#                 fire.ref('ranks/students/' + aP[m][a].mainly + '/' + aP[m][a].uID).update({
#                     rank: rank,
#                     percentile: percentile,
#                     name: resp.users[`${aP[m][a].uID}`].details.name
#                 });
#             }
#         }
#         res.locals.success = 'Data has been analyzed Successfully.';
#         next();
#     })
# }