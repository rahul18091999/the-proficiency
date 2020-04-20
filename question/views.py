from django.shortcuts import render
from exam.views import database
# Create your views here.


def question(request):
    subjectData = database.child('subjects').get()
    teacherData = database.child('teachers').get()
    data=[]
    subjectid = []
    topicName = []
    teacher = []
    k = 0
    for i in subjectData:
        if(i.key() != 'free'):
            subjectid.append({'id': i.key(), 'name': i.val()['details']['name'], 'index': k})

            topic = i.val()['topics']
            t = []
            for j in topic:
                if(j != 'free'):
                    t.append({'id': j, 'name': topic[j]['details']['name']})
                    topicName.append(t)
                    k += 1

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
        print(optc)
       
        if(ques!="" and opt1!="" and opt2!="" and opt3!="" and opt4!="" and optc is not None and subject is not None and teach is not None and topic is not None):
            pass
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
            'error':'Please check all the Details again.',
            }   
            

    return render(request, 'addQues.html', {'subject': subjectid, 'topic': topicName, 'teach': teacher,'data':data})


def addquestion(request):
    if request.method == "POST":
        ques = request.POST.get('ques')
        opt1 = request.POST.get('opt1')
        opt2 = request.POST.get('opt2')
        opt3 = request.POST.get('opt3')
        opt4 = request.POST.get('opt4')
        teacher = request.POST.get('teacher')
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')

        data = {
            'question': ques,
            'opt1': opt1,
            'opt2': opt2,
            'opt3': opt3,
            'opt4': opt4,
            'teacher': teacher,
            'subject': subject,
            'topic': topic,
        }
        if (ques == "" ):
            error = "pllease fill the below"
            data['error'] = error
            return render(request, 'addQues.html' , data)
        elif (opt1 == "" ):
            error = "pllease fill the below"
            data['error'] = error
            return render(request, 'addQues.html' , data)
        elif (opt3 == "" ):
            error = "pllease fill the below"
            data['error'] = error
            return render(request, 'addQues.html' , data)
        elif (opt3 == "" ):
            error = "pllease fill the below"
            data['error'] = error
            return render(request, 'addQues.html' , data)
        elif (opt4 == "" ):
            error = "pllease fill the below"
            data['error'] = error
            return render(request, 'addQues.html' , data)
        elif ( teacher ==None or subject == None or topic == None):
            error = "please select the below"
            data['error'] = error
            return render(request, 'addQues.html',data)
        else:
            return render(request, 'addQues.html')