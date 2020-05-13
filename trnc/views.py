from django.shortcuts import render,redirect
from exam.views import database, checkpermission
# Create your views here.
def viewTrans(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    trans = database.child('trnc').get()
    l = []
    if trans.val():
        for i in trans:
            l.append(
                {
                    'id': i.key(),
                    'name':i.val()['CUST_ID'].split("@")[1],
                    'TXN_AMOUNT': i.val()['TXN_AMOUNT'],
                }
            )
    return render(request, './trnc/viewTrns.html', {'data': l})


def seeTrns(request):
    c = checkpermission(request, request.path)
    if(c == -1):
        return redirect('/')
    elif(c == 0):
        return redirect('/home')
    idd = request.GET.get('id')
    tran = database.child('trnc').get()
    return render(request, './trnc/viewTran.html', {'data': tran.val()[idd]})