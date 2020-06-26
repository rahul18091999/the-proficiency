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
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        sp=request.POST.get('sp')
        if date and time and title and sp and desc:
            dat = date[8:]+date[5:7]+date[:4]
            NLE = database.child('exams').child('NLE').child(dat)
            NLE.update(
                {
                    'time': time,
                    'sp':int(sp)
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
                                     database.child('exams').child('NLE').child(dat).child('mainly').child(j).child('questions').update(
                                        {
                                            'free':1
                                        }
                                    )
            data = database.child('users').get().val()
            token=[]
            td = data
            from datetime import datetime
            time_now = int(datetime.now().timestamp()*1000)
            
            tid = {}
            if data:
                temp = database.child('notifications').child('free').shallow().get().val()
                if temp:
                    idd = temp
                else:
                    idd = 100000000000000
                for j in data:
                    tid[j] = 'done'
                    if 'notifications' in data[j]:
                        
                        if 'token' in data[j]['notifications']:
                        
                            token.append(data[j]['notifications']['token'])
                        

                    else:
                        td[j]['notifications']={}
                    if 'notes' not in data[j]['notifications']:
                        td[j]['notifications']['notes']={}
                    td[j]['notifications']['notes'][idd]=time_now
            if token:
                print(token)
                token.append('EfadsfadsfasdfasdxponentPushfasdTofsadfskfadssdafsdfen[4iSHToD76BENf7-ujv4hcN')
                import requests
                r = requests.post('https://exp.host/--/api/v2/push/send',
                headers={
                    "HTTP_ACCEPT":'application/json',
                    "HTTP_ACCEPT_ENCODING":'gzip, deflate',
                    "HTTP_HOST":'the-proficiency.com',
                    'Content-type': 'application/json'
                },
                json={
                    'to':token,                        
                      'title': title,                  
                      'body': desc,             
                      'priority': "high",            
                      'sound':"default",              
                      'channelId':"default",   

                })
                print(r)
                import ast
                d = ast.literal_eval(r.text)['data']
                if d[0]['status'] == 'ok':
                    database.child('notifications').child(idd).update({
                        'by':request.session['user'],
                        'discription':desc,
                        'time':time_now,
                        'title':title,
                        'to':'users',
                        'ids':tid
                    })
                    database.child('notifications').update({'free':idd+1})
                    database.child('/').update({'users':td})
       
            data = {
                'date': "",
                'time': "",
                'title':"",
                'dis':"",
                'sp':""
            }
            success = "NLE exam added successfully"
            data['success'] = success
            return render(request, './exams/addNLE.html', data)
        else:
            data = {
                'date': date,
                'time': time,
                'title':title,
                'dis':desc,
                'sp':sp
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
        print(date)
        sp=request.POST.get('sp')
        if date and time and sp:
            dat = date[8:]+date[5:7]+date[:4]
            print(dat)
            NLE = database.child('exams').child('dailyTime').child(dat)
            NLE.update(
                {
                    'time': time,
                    'sp':int(sp)
                }
            )
            data = {
                'name': "",
                'dis': "",
                'sp':"",
            }
            success = "Daily Exam added successfully"
            data['success'] = success
            return render(request, './exams/addDaily.html', data)
        else:
            data = {
                'name': date,
                'dis': time,
                'sp':sp
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/addDaily.html', data)
    else:
        return render(request, './exams/addDaily.html')

def viewDaily(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    d = database.child('exams').child('dailyTime').get()
    l=[]
    if d.val():
        for i in d:
            dat=i.key()
            date=dat[4:]+"-"+dat[2:4]+"-"+dat[:2]
            time=i.val()['time']
            l.append({'date':date,'time':time,'sp':i.val()['sp'],'id':i.key()})
    return render(request,'./exams/viewDaily.html',{'data':l})

def viewNLEs(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    d = database.child('exams').child('NLE').get()
    l=[]
    if d.val():
        for i in d:
            dat=i.key()
            date=dat[4:]+"-"+dat[2:4]+"-"+dat[:2]
            time=i.val()['time']
            l.append({'date':date,'time':time,'sp':i.val()['sp']})
    return render(request,'./exams/viewNLEs.html',{'data':l})
            

def addNLEQues(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    nledata=database.child('exams').child('NLE').get()
    mainlydata = database.child('prepration').get().val()
    date = nledata.val().keys()
    l=[]
    if date:
        for i in date:
            l.append({'value':i,'date':i[4:]+'-'+i[2:4]+'-'+i[:2]})
        l.sort(key=lambda x:x['date'])
        value = []
        for i in l:
            value.append(i['value'])
    if l:
        m=[]
        for i in l:
            n=[]
            if i['value']:
                for j in nledata.val()[i['value']]['mainly']:
                    
                    n.append( {'value':j,'name':mainlydata[j[:6]]['mainly'][j]['details']['name']})
            m.append(n)
    if request.method == "POST":
        ques = request.POST.get('ques')
        opt1 = request.POST.get('opt1')
        opt2 = request.POST.get('opt2')
        opt3 = request.POST.get('opt3')
        opt4 = request.POST.get('opt4')
        NLE = request.POST.get('NLE')
        mainly = request.POST.get('mainly')
        if(ques != "" and opt1 != "" and opt2 != "" and opt3 != "" and opt4 != "" and NLE is not None and mainly is not None):
            print('Hello')
            free = database.child('exams').child('NLE').child(NLE).child('mainly').child(mainly).child('questions').child('free').get().val()
            database.child('exams').child('NLE').child(NLE).child('mainly').child(mainly).child('questions').child(free).update({
                'id': free,
                'opt1': opt1,
                'opt2':opt2 ,
                'opt3':opt3 ,
                'opt4':opt4 ,
                'question':ques 

            })
            database.child('exams').child('NLE').child(NLE).child('mainly').child(mainly).child('questions').update({'free':free+1})
            data={
                'question': "",
                'opt1': "",
                'opt2': "",
                'opt3': "",
                'opt4': "",
                'success': 'data submitted successfully',
            }
            return render(request,'./exams/addNLEQues.html', {'date': l, 'mainly': m,'value':value,'data':data})
        else:
            data = {
                'question': ques,
                'opt1': opt1,
                'opt2': opt2,
                'opt3': opt3,
                'opt4': opt4,
                'error': 'Please check all the Details again.',
            }
            return render(request, './exams/addNLEQues.html', {'date': l, 'mainly': m,'value':value,'data':data})

    return render(request, './exams/addNLEQues.html', {'date': l, 'mainly': m,'value':value})


def viewCoupons(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    coupans = database.child('coupons').get()
    l = []
    if coupans.val():
        for i in coupans:
            l.append(
                {
                    'name': i.key(),
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
    if rank.val():
        for i in rank:
            count = max(count,len(i.val()))
    if request.method == "POST":
        name = request.POST.get('name')
        sp = request.POST.get('sp')
        alll = request.POST.get('all')
        if  not alll:
            rmax = request.POST.get('rmax')
            rmin = request.POST.get('rmin')

        date = request.POST.get('date')
        mini = request.POST.get('min')
        if alll:
            if name and sp and date and mini:
                pass
            else:
                data = {
                'name': name,
                'sp': sp,
                'min': mini,
                'date': date,
                 }
                error = "Please fill all details."
                data['error'] = error
                return render(request,'./exams/addCoupon.html', {'data': data,'count':count})

        elif name and sp and rmin and rmax and date and mini != "":
            if(rmin>rmax):
                data = {
                'name': name,
                'sp': sp,
                'min': mini,
                'rmax': rmax,
                'rmin': rmin,
                'date': date,
                }
                error = "Min must be greater than Max."
                data['error'] = error
                return render(request,'./exams/addCoupon.html', {'data': data,'count':count})
            database.child('coupons').child(name).update(
                {
                    'expDate': date,
                    'minAmt': mini,
                    'sp': sp,
                }
            )
            idd = database.child('ranks').child('students').get()
            l={}
            for i in idd:
                if(i.val()):
                    for j in i.val():
                        r=i.val()[j]['rank']
                        if(r>=int(rmin) and r<=int(rmax)):
                            l[j]=False
            database.child('coupons').child(name).update({'to': l})
            data = {
                'name': "",
                'sp': "",
                'min': "",
                'max': "",
                'date': "",
            }
            success = "Coupon added successfully."
            data['success'] = success
            
            return render(request,'./exams/addCoupon.html',{'data': data,'count':count})
        else:
            data = {
                'name': name,
                'sp': sp,
                'min': mini,
                'rmax': rmax,
                'rmin': rmin,
                'date': date,
            }
            error = "Please fill all details."
            data['error'] = error
            return render(request,'./exams/addCoupon.html', {'data': data,'count':count})

    else:
        return render(request,'./exams/addCoupon.html',{'count':count})

def viewCouponsTo(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    idd = request.GET.get('cid')
    dat = database.child('coupons').child(idd).get()
    l=[]
    l.append(
        {
            'name': dat.key(),
        }
    )
    print(dat.key())
    # if 'to' in dat:
    to = database.child('coupons').child(idd).child('to').get()
    print(to)
    for i in to:
        l.append(
            {
                'id': i.key(),
                'status': i.val(),
            }
        )
    return render(request, './exams/viewTo.html', {'data': l})


def viewNleQues(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    d=request.GET.get('qid')
    nle=d[8:]+d[5:7]+d[:4]
    data=database.child('exams').child('NLE').child(nle).child('mainly').get()
    mainlydata = database.child('prepration').get().val()
    mainly = (data.val().keys())
    if mainly:
        l=[]
        for j in mainly:
            f=[]
            for m in data.val()[j]['questions']:
                if m!="free":
                    if 'optC' in (data.val()[j]['questions'][m]):
                        f.append({'id':m,'ans':data.val()[j]['questions'][m]['optC']})
                    else:
                        f.append({'id':m,'ans':'false'})
            print(j)

            l.append({'name':mainlydata[j[:6]]['mainly'][j]['details']['name'],'id':j,'question':f})


    return render(request,'./exams/viewNLEQuestions.html',{'mainly':l,'nle':nle})

def addAnsKey(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    nle=request.GET.get('nle')
    mid=request.GET.get('mid')
    count = database.child('exams').child('NLE').child(nle).child('mainly').child(mid).child('questions').child('free').shallow().get().val()
    if request.method == 'POST':
        ans=[]
        for i in range(1,count):
            a=request.POST.get('optC'+str(i))
            if a:
                ans.append(a)
            else:
                return render(request,'./exams/addAnsKey.html',{'count':range(1,count),'error':"Please select all ans."})
        for index,item in enumerate(ans):
            database.child('exams').child('NLE').child(nle).child('mainly').child(mid).child('questions').child(index+1).update({'optC':item})
        return redirect('/exams/viewNleQues?qid='+nle[4:]+'-'+nle[2:4]+'-'+nle[:2])
    return render(request,'./exams/addAnsKey.html',{'count':range(1,count)})
    


def editDaily(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    date=request.GET.get('id')
    data = database.child('exams').child('dailyTime').child(date).get().val()
    data['date']=date[:2]+"-"+date[2:4]+"-"+date[4:]
    if request.method=="POST":
        time = request.POST.get('time')
        sp=request.POST.get('sp')
        if time and sp:
            NLE = database.child('exams').child('dailyTime').child(date)
            NLE.update(
                {
                    'time': time,
                    'sp':int(sp)
                }
            )
            
            success = "Daily Exam Edited successfully"
            data['success'] = success
            return redirect('/exams/viewDaily')
        else:
            data = {
                'date': date[:2]+"-"+date[2:4]+"-"+date[4:],
                'time': time,
                'sp':sp
            }
            error = "please fill the details"
            data['error'] = error
            return render(request, './exams/editDaily.html', data)
    return render(request, './exams/editDaily.html', data)


def viewExamStudent(request):
    c=checkpermission(request,request.path)
    print(c)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    d=database.child('/').get()
    NLEdate=list(d.val()['exams']['NLE'].keys())
    for i in range(len(NLEdate)):
        NLEdate[i]=NLEdate[i][4:]+'-'+NLEdate[i][2:4]+'-'+NLEdate[i][:2]
    NLEdate.sort()
    dailyTimedate=list(d.val()['exams']['dailyTime'].keys())
    for i in range(len(dailyTimedate)):
        dailyTimedate[i]=dailyTimedate[i][4:]+'-'+dailyTimedate[i][2:4]+'-'+dailyTimedate[i][:2]
    dailyTimedate.sort()

    if request.method=="POST":
        exam=request.POST.get('exam')
        date = request.POST.get('date')
        return redirect('/exams/viewExamStu?exam='+exam+'&date='+date)
    return render(request,'./exams/viewExamStudent.html',{'NLE':NLEdate,'daily':dailyTimedate})


def viewExamStu(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    exam=request.GET.get('exam')
    date = request.GET.get('date')
    d=database.child('/').get()
    d=d.val()
    l=[]
    for i in d['users']:
        if 'exams' in d['users'][i]:
            if exam in d['users'][i]['exams']:
                if date in d['users'][i]['exams'][exam]:
                    l.append({'id':i,'status':True})
                else:
                    l.append({'id':i,'status':False})
            else:
                l.append({'id':i,'status':False})
        else:
            l.append({'id':i,'status':False})
    return render(request,'./exams/viewExamStu.html',{'data':l})


def viewStudentRank(request):
    c=checkpermission(request,request.path)
    if(c==-1):
        return redirect('/')
    elif(c==0):
        return redirect('/home')
    
    d=database.child('/').get()
    NLEdate=list(d.val()['exams']['NLE'].keys())
    for i in range(len(NLEdate)):
        NLEdate[i]=NLEdate[i][4:]+'-'+NLEdate[i][2:4]+'-'+NLEdate[i][:2]
    NLEdate.sort()
    dailyTimedate=list(d.val()['exams']['dailyTime'].keys())
    for i in range(len(dailyTimedate)):
        dailyTimedate[i]=dailyTimedate[i][4:]+'-'+dailyTimedate[i][2:4]+'-'+dailyTimedate[i][:2]
    dailyTimedate.sort()
    mainlyData = d.val()['prepration']
    mainlyList=[]
    for i in mainlyData:
        if i!="free":
            for j in mainlyData[i]['mainly']:
                if j!="free":
                    mainlyList.append(j)
    if request.method=="POST":
        exam=request.POST.get('exam')
        date = request.POST.get('date')
        mainly = request.POST.get('mainly')
        print(exam,date,mainly)
        return redirect('/exams/viewStudentRankk?exam='+exam+'&date='+date+'&mainly='+mainly)
        
    return render(request,'./exams/viewStudentRankk.html',{'NLE':NLEdate,'daily':dailyTimedate,'mainly':mainlyList})
    

def viewStudentRankk(request):
    exam=request.GET.get('exam')
    date = request.GET.get('date')
    mainly = request.GET.get('mainly')
    data = database.child('ranks').child('students').child(mainly).get().val()
    l=[]
    for i in data:
        l.append({
            'id':i,
            'name':data[i]['name'],
            'percentile':data[i]['percentile'],
            'phone':data[i]['phone'],
            'rank':data[i]['rank'],

        })
    return render(request,'./exams/viewStudentRank.html',{'data':l})

def viewNleQues2(request):
    # c=checkpermission(request,request.path)
    # if(c==-1):
    #     return redirect('/')
    # elif(c==0):
    #     return redirect('/home')
    d=request.GET.get('qid')
    nle=d[8:]+d[5:7]+d[:4]
    data=database.child('exams').child('NLE').child(nle).child('mainly').get()
    mainlydata = database.child('prepration').get().val()
    mainly = (data.val().keys())
    if mainly:
        l=[]
        for j in mainly:
            f=[]
            for m in data.val()[j]['questions']:
                if m!="free":
                    print(data.val()[j]['questions'][m])
                    if 'optC' in (data.val()[j]['questions'][m]):
                        f.append({'id':m,'ques':data.val()[j]['questions'][m]['question'],'opt1':data.val()[j]['questions'][m]['opt1'],'opt2':data.val()[j]['questions'][m]['opt2'],'opt3':data.val()[j]['questions'][m]['opt3'],'opt4':data.val()[j]['questions'][m]['opt4'],'ans':chr(ord('`')+int(data.val()[j]['questions'][m]['optC'][3]))})
                    else:
                        f.append({'id':m,'ans':'false'})
            

            l.append({'name':mainlydata[j[:6]]['mainly'][j]['details']['name'],'id':j,'question':f})


    return render(request,'./exams/viewNLEQuestions2.html',{'mainly':l,'nle':nle})


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')