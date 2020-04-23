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
                check = "false"

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
    for i in question:
        if(i.key()!='free'):
            questiondata.append({'id':i.key(),'approved':i.val()['details']['approved'],'by':i.val()['details']['by']})
            
    print(questiondata)
    return render(request,'viewQues.html',{'question':questiondata})