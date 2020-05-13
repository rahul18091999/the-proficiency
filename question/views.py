from django.shortcuts import render,redirect
from exam.views import database,getuserdetail,checkpermission
# Create your views here.
import json
def question(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    
    subjectData = database.child('subjects').get()
    teacherData = database.child('teachers').get()
    data = []
    subjectid = []
    topicName = []
    teacher = []
    k = 0
    if subjectData.val():
        for i in subjectData:
            if(i.key() != 'free'):
                subjectid.append({"id": i.key(), "name": i.val()[
                                'details']['name'], "index": k})
                k += 1
                topic = i.val()['topics']
                t = []
                for j in topic:
                    if(j != 'free'):
                        t.append({'id': j, 'name': topic[j]['details']['name']})
                topicName.append(t)
    if teacherData.val():       
        for i in teacherData:
            if (i.key() != 'qBank'):
                teacher.append(
                    {
                        
                        'tId': i.key(),
                        'name': i.val()['details']['name']
                    }
                )

    if request.method == "POST":
        ques = request.POST.get('ques')
        opt1 = request.POST.get('opt1')
        opt2 = request.POST.get('opt2')
        opt3 = request.POST.get('opt3')
        opt4 = request.POST.get('opt4')
        optc = request.POST.get('optC')
        teach = request.POST.get('teacher')
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')
        subj = (request.POST.get('result'))
        user=getuserdetail(request.session['us'])
        userid=request.session['user']
        
        if(ques != "" and opt1 != "" and opt2 != "" and opt3 != "" and opt4 != "" and optc is not None and subject is not None and teach is not None and topic is not None):
            import ast
            subjId = ast.literal_eval(subj)[int(subject)]['id']
            free = database.child('questions').child(
                'free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000000001
            if teach == "qBank":
                check = "true"
            else:
                check = "review"

            database.child('questions').child("q"+str(tempid)).child('details').update(
                {   
                    'approved': check,
                    'by': teach,
                    'question': ques,
                    'opt1': opt1,
                    'opt2': opt2,
                    'opt3': opt3,
                    'opt4': opt4,
                    'optC': optc, 
                    'typer':request.session['user'] ,
                    'topic':topic 
                }
            )
            database.child('teachers').child(teach).child('questions').child("q"+str(tempid)).update({'topic': topic})
            database.child('questions').update({'free':tempid+1})
            database.child('subjects').child(subjId).child('teachers').child(teach).child('topics').child(topic).child('questions').child("q"+str(tempid)).update(
                {
                    'by':teach
                }
            )
            database.child('subjects').child(subjId).child('topics').child(topic).child('questions').child("q"+str(tempid)).update(
                 {
                    'by':teach
                }
            )
            database.child(user[0]).child(userid).child('questionsAdded').child("q"+str(tempid)).update(
                {
                    'by':teach,
                    'topic':topic,
                }
            )

            data={
                'question': "",
                'opt1': "",
                'opt2': "",
                'opt3': "",
                'opt4': "",
                'teacher': "",
                'subject': "",
                'topic': "",
                'success': 'data submitted successfully',
            }
            return render(request,"addQues.html",{'subject': subjectid, 'topic': topicName, 'teach': teacher, 'data': data})
        else:
            data = {
                'question': ques,
                'opt1': opt1,
                'opt2': opt2,
                'opt3': opt3,
                'opt4': opt4,
                'teacher': teach,
                'subject': subject,
                'topic': topic,
                'error': 'Please check all the Details again.',
            }
    return render(request, 'addQues.html', {'subject': subjectid, 'topic': topicName, 'teach': teacher, 'data': data})



def viewQuestion(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    question=database.child('questions').get()
    questiondata=[]
    if question.val():
        for i in question:
            if(i.key()!='free'):
                questiondata.append({'id':i.key(),'approved':i.val()['details']['approved'],'by':i.val()['details']['by']})
        
        return render(request, './question/viewquestion.html',{'question':questiondata})
    else:
        return render(request, './question/viewquestion.html')


def seeQues(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    qid = request.GET.get('qid')
    data = database.child('questions').child(qid).child('details').get().val()
    pre = request.session['us']
    idd = request.session['user']
    print(data)
    if(data and( pre == '15' or pre == '13' or idd == data['by'] or ( 'typer' in data and idd == data['typer'] ) )):
        tname = database.child('teachers').child(data['by']).child('details').child('name').get().val()
        tyname=''
        if 'typer' in data:
            tyname = database.child('typers').child(data['typer']).child('details').child('name').get().val()
        topic=''
        sname=''
        sid=''
        if 'topic' in data:
            d = database.child('subjects').child(data['topic'][:5]).get().val()
            sid = data['topic'][:5]
            sname = d['details']['name']
            topic = d['topics'][data['topic']]['details']['name']
        return render(request,'./question/seeQues.html',{'data':data,'tname':tname,'tyname':tyname,'qid':qid,'topic':topic,'sid':sid,'sname':sname})
    return redirect('/')


def editQues(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    qid = request.GET.get('qid')
    data = database.child('questions').child(qid).child('details').get().val()
    pre = request.session['us']
    idd = request.session['user']
    if(data and( pre == '15' or pre == '13' or ( 'typer' in data and idd == data['typer'] ))):
        tname = database.child('teachers').child(data['by']).child('details').child('name').get().val()
        sid = data['topic'][:5]
        sdata = database.child('subjects').child(sid).get().val()
        sname = sdata['details']['name']
        topic = sdata['topics'][data['topic']]['details']['name']
        if request.method == 'POST':
            ques = request.POST.get('ques')
            opt1 = request.POST.get('opt1')
            opt2 = request.POST.get('opt2')
            opt3 = request.POST.get('opt3')
            opt4 = request.POST.get('opt4')
            optc = request.POST.get('optC')
            if(ques and opt1 and opt2 and opt3 and opt4):
                database.child('questions').child(qid).child('details').update(
                    {   
                    
                    'question': ques,
                    'opt1': opt1,
                    'opt2': opt2,
                    'opt3': opt3,
                    'opt4': opt4,
                    'optC': optc, 
                    }
                )
                data = database.child('questions').child(qid).child('details').get().val()
                return render(request,'./question/editQues.html',{'data':data,'tname':tname,'sid':sid,'sname':sname,'topic':topic,'success':"Edit Successfully. "})
            else:
                return render(request,'./question/editQues.html',{'data':data,'tname':tname,'sid':sid,'sname':sname,'topic':topic,'error':"Please fill all the details."})
        return render(request,'./question/editQues.html',{'data':data,'tname':tname,'sid':sid,'sname':sname,'topic':topic})
    return redirect('/')

   