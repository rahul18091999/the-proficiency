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
            import requests
            import ast
            ip, is_routable = get_client_ip(request)
            # ipp = "157.36.168.57"
            r = requests.get("http://ip-api.com/json/"+ip)
            cityy = ast.literal_eval(r.text)['city']
            lastIP = request.session['ipp']
            
            if(ip!=lastIP):
                city = request.session['cityyy']
                if (cityy != city):
                    return redirect('/logout')
                else:
                    del request.session['ipp']
                    del request.session['cityyy']
                    request.session['ipp']
                    request.session['cityyy']
        return response
    return middleware
