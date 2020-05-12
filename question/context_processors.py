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
            lastIP = database.child(request.session['table']).child(request.session['number']).get().val()
            ip, is_routable = get_client_ip(request)
            if(ip!=lastIP['lastIP']):
                return redirect('/logout')
        return response
    return middleware
