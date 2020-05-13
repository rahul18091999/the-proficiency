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
            from django.contrib.gis.geoip2 import GeoIP2
            g = GeoIP2()
            response=g.city("")
            print(response)
            print(format(response['city']))
            lastIP = request.session['ip']
            ip, is_routable = get_client_ip(request)
            response=g.city(lastIP)
            response1=g.city(ip)
            if(format(response1['city'])!=format(response['city'])):
                return redirect('/logout')
        return response
    return middleware
