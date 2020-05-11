from django.shortcuts import render,redirect
from exam.views import database, checkpermission
# Create your views here.
def addBU(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home') 
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        if (name != "" and dis != ""):
            free = database.child('boards').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 10000
            database.child('boards').child("bU"+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('boards').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "Board added successfully."
            data['success'] = success
            return render(request, './academics/addBU.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addBU.html', data)
    else:
        return render(request, './academics/addBU.html')

def addPrepFor(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        if (name != "" and dis != ""):
            free = database.child('prepration').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000
            database.child('prepration').child("pP"+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('prepration').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "Preparing For added successfully."
            data['success'] = success
            return render(request, './academics/addPrepFor.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addPrepFor.html', data)
    else:
        return render(request, './academics/addPrepFor.html')

def addHd(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        if (name != "" and dis != ""):
            free = database.child('hDegree').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000
            database.child('hDegree').child("hD"+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('hDegree').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "High Degree added successfully."
            data['success'] = success
            return render(request, './academics/addHD.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addHD.html', data)
    else:
        return render(request, './academics/addHD.html')

def addSubject(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        if (name != "" and dis != ""):
            free = database.child('subjects').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000
            database.child('subjects').child("s"+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('subjects').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "Subject added successfully."
            data['success'] = success
            return render(request, './academics/addSubject.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addSubject.html', data)
    else:
        return render(request, './academics/addSubject.html')

def addTopic(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    subdata=database.child('subjects').get()
    subjectdata=[]
    if subdata.val():
        for i in subdata:
            if i.key()!='free':
                subjectdata.append({'id':i.key(),'name':subdata.val()[i.key()]['details']['name']})
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        sub=request.POST.get('subject')
        if (name != "" and dis != "" and sub is not None):
            free = database.child('subjects').child(sub).child('topics').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 1000
            database.child('subjects').child(sub).child('topics').child(sub+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('subjects').child(sub).child('topics').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "Topic added successfully."
            data['success'] = success
            data['data']=subjectdata
            return render(request, './academics/addTopic.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                    'data':subjectdata
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addTopic.html', data)
    else:
        return render(request, './academics/addTopic.html',{'data':subjectdata})

def addMainly(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    prepdata=database.child('prepration').get()
    preprationdata=[]
    if prepdata.val():
        print(prepdata)
        for i in prepdata:
            if i.key()!='free':
                preprationdata.append({'id':i.key(),'name':prepdata.val()[i.key()]['details']['name']})
    if request.method == "POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        prep=request.POST.get('prepration')
        if (name != "" and dis != "" and prep is not None):
            free = database.child('prepration').child(prep).child('mainly').child('free').shallow().get().val()
            if free:
                tempid = free
            else:
                tempid = 100
            database.child('prepration').child(prep).child('mainly').child(prep+str(tempid)).child('details').update(
                {
                    'name': name,
                    'dis': dis,
                }
            )
            database.child('prepration').child(prep).child('mainly').update({'free': tempid+1})
            data = {
                    'name': '',
                    'dis': '',
                }
            success = "Mainly added successfully."
            data['success'] = success
            data['data']=preprationdata
            return render(request, './academics/addMainly.html', data)
        else:
            data = {
                    'name': name,
                    'dis': dis,
                    'data':preprationdata
                }
            error = "Please fill the details."
            data['error'] = error
            return render(request, './academics/addMainly.html', data)
    else:
        return render(request, './academics/addMainly.html',{'data':preprationdata})


def viewBU(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('boards').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                l.append(
                    {
                        'id': i.key(),
                        'name': i.val()['details']['name'],
                        'dis': i.val()['details']['dis']
                    }
                )
    return render(request, './academics/viewBU.html',{'data': l})
def viewHd(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('hDegree').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                l.append(
                    {
                        'id': i.key(),
                        'name': i.val()['details']['name'],
                        'dis': i.val()['details']['dis']
                    }
                )
    return render(request, './academics/viewHD.html',{'data': l})

def viewPrepFor(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('prepration').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                l.append(
                    {
                        'id': i.key(),
                        'name': i.val()['details']['name'],
                        'dis': i.val()['details']['dis']
                    }
                )
    return render(request, './academics/viewPrepFor.html',{'data': l})

def viewSubjects(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('subjects').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                l.append(
                    {
                        'id': i.key(),
                        'name': i.val()['details']['name'],
                        'dis': i.val()['details']['dis']
                    }
                )
    return render(request, './academics/viewSubjects.html',{'data': l})

def viewTopic(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('subjects').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                name=i.val()['details']['name']
                if 'topics' in i.val():
                    t=i.val()['topics']
                    for j in t:
                        if j !='free':
                            l.append({'id':j,'name':t[j]['details']['name'],'dis':t[j]['details']['dis'],'sub':name})
                print(name)
    return render(request, './academics/viewTopics.html',{'data': l})

def viewMainly(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    data = database.child('prepration').get()
    l=[]
    if data.val():
        for i in data:
            if (i.key() != 'free'):
                name=i.val()['details']['name']
                if 'mainly' in i.val():
                    t=i.val()['mainly']
                    for j in t:
                        if j !='free':
                            l.append({'id':j,'name':t[j]['details']['name'],'dis':t[j]['details']['dis'],'sub':name})
                print(name)
    return render(request, './academics/viewMainly.html',{'data': l})



def linksub(request):
    mid  = request.GET.get('id')
    mname = database.child('prepration').child(mid[:6]).child('mainly').child(mid).child('details').get().val()
    mname = mname['name']
    msub = database.child('prepration').child(mid[:6]).child('mainly').child(mid).child('subjects').shallow().get().val()
    sub = database.child('subjects').get().val()
    subdata = []
    if not msub:
        msub=[]
    if sub:
        for i in sub:
            if i !='free':
                subdata.append({
                    'id':i,
                    'name':sub[i]['details']['name'],
                    'dis':sub[i]['details']['dis'],
                    'ul':'Unlink' if i in msub else 'Link'
                })
    return render(request,'./academics/linksub.html',{'data':subdata,'name':mname,'mid':mid})

def sublink(request):
    mid = request.GET.get('mid')
    sid = request.GET.get('sid')
    l = request.GET.get('l')
    if (l=='Link'):
        database.child('prepration').child(mid[:6]).child('mainly').child(mid).child('subjects').child(sid).update({'active':'true'})
    else:
        database.child('prepration').child(mid[:6]).child('mainly').child(mid).child('subjects').child(sid).remove()
    return redirect('/academics/linksub?id='+mid)