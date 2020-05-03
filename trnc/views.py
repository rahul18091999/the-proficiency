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
    return render(request, './users/viewTrns.html', {'data': l})


def seeTrns(request):
    idd = request.GET.get('id')
    tran = database.child('trnc').get()
    l = []
    l.append(
        {
            'BANKNAME': tran.val()[idd]['BANKNAME'],

            'TXNID': tran.val()[idd]['BANKTXNID'],


            'CUST_ID': tran.val()[idd]['CUST_ID'],


            'EMAIL': tran.val()[idd]['EMAIL'],


            'GATEWAY': tran.val()[idd]['GATEWAYNAME'],


            'MID': tran.val()[idd]['MID'],

            'MOBILE__NO': tran.val()[idd]['MOBILE_NO'],

            'ORDERID': tran.val()[idd]['ORDERID'],
            'ORDER_ID': tran.val()[idd]['ORDER_ID'],
            'PAYMENTMODE': tran.val()[idd]['PAYMENTMODE'],
            'REFUNDAMT': tran.val()[idd]['REFUNDAMT'],
            'RESPCODE': tran.val()[idd]['RESPCODE'],
            'RESPMSG': tran.val()[idd]['RESPMSG'],
            'STATUS': tran.val()[idd]['STATUS'],
            'TXNAMOUNT': tran.val()[idd]['TXNAMOUNT'],
            'TXNDATE': tran.val()[idd]['TXNDATE'],
            'TXNID': tran.val()[idd]['TXNID'],
            'TXNTYPE': tran.val()[idd]['TXNTYPE'],
            'TXN_AMOUNT': tran.val()[idd]['TXN_AMOUNT'],
            'cmnts': tran.val()[idd]['cmnts'],
            'coupon': tran.val()[idd]['coupon'],
            'sp': tran.val()[idd]['sp'],


        }
    )
    return render(request, './users/viewTran.html', {'data': l})