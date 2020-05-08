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
        print(NLE,mainly)
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
        rmin = request.POST.get('rmin')
        rmax = request.POST.get('rmax')
        date = request.POST.get('date')
        mini = request.POST.get('min')
        if name and sp and rmin and rmax and date and mini != "":
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
                            l[j]='false'
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


            l.append({'name':mainlydata[j[:6]]['mainly'][j]['details']['name'],'id':j,'question':f})


    return render(request,'./exams/viewNLEQuestions.html',{'mainly':l,'nle':nle})

def addAnsKey(request):
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
    



    