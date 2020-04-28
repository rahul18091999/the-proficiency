from django.shortcuts import render,redirect
from exam.views import database, checkpermission, getuserdetail

# Create your views here.


def addNLEs(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time !="":
            dat = date[8:]+date[5:7]+date[:4]
            NLE = database.child('exams').child('NLE').child(dat)
            NLE.update(
                {
                    'time': time,
                }
            )
            print("time")
            data = database.child('prepration').get()
            if data.val():
                for i in data:
                    if (i.key() != 'free'):
                        if 'mainly' in i.val():
                            t = i.val()['mainly']
                            for j in t:
                                if j != 'free':
                                     database.child('exams').child('NLE').child(dat).child('mainly').child(j).update(
                                        {
                                            'name': t[j]['details']['name'],
                                            'dis': t[j]['details']['dis']
                                        }
                                    )
            data = {
                'name': "",
                'dis': "",
            }
            success = "submitted successfully"
            data['success'] = success
            return render(request, './exams/addNLE.html', data)
        else:
            data = {
                'name': date,
                'dis': time,
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/addNLE.html', data)
    else:
        return render(request, './exams/addNLE.html')



def daily(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time !="":
            dat = date[8:]+date[5:7]+date[:4]
            print(dat)
            NLE = database.child('exams').child('dailyTime').child(dat)
            print("xyz")
            NLE.update(
                {
                    'time': time,
                }
            )
            data = {
                'name': "",
                'dis': "",
            }
            success = "submitted successfully"
            data['success'] = success
            return render(request, './exams/addDaily.html', data)
        else:
            data = {
                'name': date,
                'dis': time,
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/addDaily.html', data)
    else:
        return render(request, './exams/addDaily.html')

def viewDaily(request):
    d = database.child('exams').child('dailyTime').get()
    l=[]
    if d.val():
        for i in d:
            dat=i.key()
            date=dat[4:]+"-"+dat[2:4]+"-"+dat[:2]
            time=i.val()['time']
            l.append({'date':date,'time':time})
    return render(request,'./exams/viewDaily.html',{'data':l})

def viewNLEs(request):
    d = database.child('exams').child('NLE').get()
    l=[]
    if d.val():
        for i in d:
            dat=i.key()
            date=dat[4:]+"-"+dat[2:4]+"-"+dat[:2]
            time=i.val()['time']
            l.append({'date':date,'time':time})
    return render(request,'./exams/viewNLEs.html',{'data':l})
            

def addNLEQues(request):
    # c=checkpermission(request,request.path)
    # if(c==-1):
    #     return redirect('/')
    # elif(c==0):
    #     return redirect('/home')
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


def viewCoupons(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    coupans = database.child('coupans').get()
    l = []
    for i in coupans:
        l.append(
            {
                'name': i,
                'exp': i.val()['expDate'],
                'min': i.val()['minAmt'],
                'sp': i.val()['sp']
            }
        )
    return render(request,'./exams/viewCoupons.html',{'data': l})

def addCoupon(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    rank = database.child('ranks').child('students').get()
    count = 0
    for i in rank:
        count += 1
    if request.method == "POST":
        name = request.POST.get['name']
        sp = request.POST.get['sp']
        no = request.POST.get['no']
        date = request.POST.get['date']
        mini = request.POST.get['min']
        if name and sp and no and date and mini != "":
            database.child('coupans').child(name).update(
                {
                    'expDate': date,
                    'minAmt': mini,
                    'sp': sp,
                }
            )
            countno = 1
            idd = database.chid('preprations').get()
            for i in idd:
                countno += countno
                if countno == no:
                    iddd = i
            database.child('coupans').child(name).child('to').update({iddd: 'false'})
            data = {
                'name': "",
                'sp': "",
                'min': "",
                'max': "",
                'date': "",
            }
            success = "submitted successfully"
            data['success'] = success
            return render(request,'./exams/addCoupan.html', data,count)
        else:
            data = {
                'name': "",
                'sp': "",
                'min': "",
                'max': "",
                'date': "",
            }
            error = "submitted successfully"
            data['error'] = error
            return render(request,'./exams/addCoupan.html', data, count)

    else:
        return render(request,'./exams/addCoupon.html',count)
