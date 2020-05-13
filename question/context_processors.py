from django.shortcuts import render, redirect
from exam.views import database
from ipware import get_client_ip
def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image = request.session['image']
        name = request.session['name']
        userid = request.session['user']
        if 'subid' in request.session:
            path = request.session['subid']
            return {
                'session': ses, 'homeimage': image, 'homename': name, 'subid': str(path)[:2],'jamura':userid
            }
        else:
            return {
                'session': ses, 'homeimage': image, 'homename': name, 'jamura':userid
            }
    except:
        return {}

def checkIp(get_response):
    def middleware(request):
        response = get_response(request)
        if request.path =="/" or request.path =='/logout':
            pass
        else:
            try:
                import requests
                import ast
                ip, is_routable = get_client_ip(request)
                from datetime import datetime
                time_now = int(datetime.now().timestamp()*1000)
                # ip = "157.36.168.57"
                
                # lastIP = '2409:4051:5:a1d5:5502:f099:9f8f:6996'
                
                lastIP = request.session['ipp']
                cip = ip.replace(".","-")
                clastip = lastIP.replace(".","-")
                if(ip!=lastIP):
                    ip1Data = database.child('ipChange').child(request.session['table']).child(request.session['number']).child(cip).get().val()
                    if not ip1Data:
                        r = requests.get("http://ip-api.com/json/"+ip)
                        ip1Data = ast.literal_eval(r.text)
                        city = ip1Data['city']
                    else:
                        city = ip1Data['city']
                    ip1Data['time']=time_now
                    ip2Data = database.child('ipChange').child(request.session['table']).child(request.session['number']).child(clastip).get().val()
                    if not ip2Data:
                        r = requests.get("http://ip-api.com/json/"+lastIP)
                        ip2Data = ast.literal_eval(r.text)
                        cityy = ip2Data['city']
                    cityy = ip2Data['city']
                    ip2Data['time']=time_now
                    # city = request.session['cityyy']
                    database.child('ipChange').child(request.session['table']).child(request.session['number']).update({clastip:ip2Data,cip:ip1Data})

                    if (cityy != city):
                        return redirect('/logout')
                    else:
                        del request.session['ipp']
                        request.session['ipp']=ip
            except:
                pass        
        return response
    return middleware
