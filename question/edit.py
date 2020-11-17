from django.shortcuts import render,redirect,HttpResponse
from exam.views import database
# Create your views here.

def edit(request):
   
    subjId = 's1000'
    dst = '12100021'
    topic = 's10001005'
    for i in range(1457,1487):
        # print(data['q100000'+   str(i)])
        qid = 'q'+str(1000000000+i)
        
        # data[qid]['details']['by']=dst
        # data[qid]['details']['approved']='review'
        # topic = data[qid]['details']['topic']
        # database.child('teachers').child(dst).child('questions').child(qid).update({'topic': topic})
        database.child('subjects').child(subjId).child('teachers').child(dst).child('topics').child(topic).child('questions').child(qid).update(
                {
                    'by':dst
                }
            )
        database.child('subjects').child(subjId).child('topics').child(topic).child('questions').child(qid).update(
                 {
                    'by':dst
                }
            )
        # database.child('typers').child('14100003').child('questionsAdded').child(qid).update(
        #         {
        #             'by':dst,
        #             'topic':topic,
        #         }
        #     )
        # database.child('teachers').child(src).child('questions').child(qid).remove()

    return HttpResponse("Hello")



def edit1(request):
    data = database.child('questions').get().val()
    typer = database.child('typers').get().val()
    from datetime import date,datetime

    time_now = int(datetime.now().timestamp()*1000)

    dat = str(date.fromtimestamp(time_now/1000))
    date = dat[0:7]
    for i in range(489,900):
        print(i)
        qid = 'q'+str(1000000000+i)
        data[qid]['details']['time'] = time_now
        print(str(data[qid]['details']['typer'])[:2])

        if str(data[qid]['details']['typer'])[:2]=='15' :
            continue
        #     d = 'superAdmin'
        # else:
        #     d='typer' 
        if  date not in typer[data[qid]['details']['typer']]['questionsAdded']:
            typer[data[qid]['details']['typer']]['questionsAdded'][date]={}
        typer[data[qid]['details']['typer']]['questionsAdded'][date][qid]=typer[data[qid]['details']['typer']]['questionsAdded'][qid]
    database.child('/').update({'questions':data,'typers':typer})
    # print(data.split['-'])
    print(date)
    print(time_now)


def edit2(request):
    data = database.child('questions').get().val()
    typer = database.child('typers').get().val()
    from datetime import date,datetime

    time_now = 1593540499634

    dat = str(date.fromtimestamp(time_now/1000))
    date = dat[0:7]
    for i in range(900,1300):
        print(i)
        qid = 'q'+str(1000000000+i)
        
       

        if qid == 'q1000000229' or str(data[qid]['details']['typer'])[:2]=='15' :
            continue
        #     d = 'superAdmin'
        # else:
        #     d='typer' 
        data[qid]['details']['time'] = time_now
        if  date not in typer[data[qid]['details']['typer']]['questionsAdded']:
            typer[data[qid]['details']['typer']]['questionsAdded'][date]={}
        typer[data[qid]['details']['typer']]['questionsAdded'][date][qid]={
                    'by':data[qid]['details']['by'],
                    'topic':data[qid]['details']['topic'],
                }
    database.child('/').update({'questions':data,'typers':typer})
     











def edit3(request):
    data = database.child('questions').get().val()
    typer = database.child('typers').get().val()
    from datetime import date,datetime

    time_now = int(datetime.now().timestamp()*1000)

    dat = str(date.fromtimestamp(time_now/1000))
    date = dat[0:7]
    for i in range(1300,1658):
        print(i)
        qid = 'q'+str(1000000000+i)
        data[qid]['details']['time'] = time_now
        print(str(data[qid]['details']['typer'])[:2])

        if qid == 'q1000000229' or str(data[qid]['details']['typer'])[:2]=='15'  :
            continue
        #     d = 'superAdmin'
        # else:
        #     d='typer' 
        if  date not in typer[data[qid]['details']['typer']]['questionsAdded']:
            typer[data[qid]['details']['typer']]['questionsAdded'][date]={}
        typer[data[qid]['details']['typer']]['questionsAdded'][date][qid]=typer[data[qid]['details']['typer']]['questionsAdded'][qid]
    database.child('/').update({'questions':data,'typers':typer})
    # print(data.split['-'])
    print(date)
    print(time_now)





# def edit2(request):
#     data = database.child('questions').get().val()
#     typer = database.child('typers').get().val()
#     time_now = 1590837446929
#     from datetime import date

#     dat = str(date.fromtimestamp(time_now/1000))
#     date = dat[0:7]
#     for i in range(200,300):
#         print(i)
#         qid = 'q'+str(1000000000+i)
#         data[qid]['details']['time'] = time_now
#         print(str(data[qid]['details']['typer'])[:2])

#         if str(data[qid]['details']['typer'])[:2]=='15' :
#             continue
#         #     d = 'superAdmin'
#         # else:
#         #     d='typer' 
#         if  date not in typer[data[qid]['details']['typer']]['questionsAdded']:
#             typer[data[qid]['details']['typer']]['questionsAdded'][date]={}
#         typer[data[qid]['details']['typer']]['questionsAdded'][date][qid]=typer[data[qid]['details']['typer']]['questionsAdded'][qid]
#     database.child('/').update({'questions':data,'typers':typer})
#     # print(data.split['-'])
#     print(date)
#     print(time_now)





# def edit2(request):
#     data = database.child('questions').get().val()
#     typer = database.child('typers').get().val()
#     time_now = 1590837446929
#     from datetime import date

#     dat = str(date.fromtimestamp(time_now/1000))
#     date = dat[0:7]
#     for i in range(200,300):
#         print(i)
#         qid = 'q'+str(1000000000+i)
#         data[qid]['details']['time'] = time_now
#         print(str(data[qid]['details']['typer'])[:2])

#         if str(data[qid]['details']['typer'])[:2]=='15' :
#             continue
#         #     d = 'superAdmin'
#         # else:
#         #     d='typer' 
#         if  date not in typer[data[qid]['details']['typer']]['questionsAdded']:
#             typer[data[qid]['details']['typer']]['questionsAdded'][date]={}
#         typer[data[qid]['details']['typer']]['questionsAdded'][date][qid]=typer[data[qid]['details']['typer']]['questionsAdded'][qid]
#     database.child('/').update({'questions':data,'typers':typer})
#     # print(data.split['-'])
#     print(date)
#     print(time_now)








