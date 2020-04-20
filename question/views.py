from django.shortcuts import render
from exam.views import database
# Create your views here.


def question(request):
    subjectData = database.child('subjects').get()
    teacherData = database.child('teachers').get()
    subjectid = []
    topicName = []
    teacher = []
    k = 0
    for i in subjectData:
        if(i.key() != 'free'):
            subjectid.append({'id': i.key(), 'name': i.val()[
                'details']['name'], 'index': k})

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
    return render(request, 'addQues.html', {'data': subjectid, 'topic': topicName, 'teach': teacher})
