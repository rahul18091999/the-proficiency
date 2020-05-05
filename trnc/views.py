from django.shortcuts import render
from exam.views import database, checkpermission
# Create your views here.
def viewTrans(request):
    trans = database.child('trnc').get()
    l = []
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
    idd = request.GET.get('id')
    tran = database.child('trnc').get()
    return render(request, './trnc/viewTran.html', {'data': tran.val()[idd]})