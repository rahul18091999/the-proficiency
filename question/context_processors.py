def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        
        path='99'
        try:
            
            path=request.GET.get('id')
        except:
            pass
        return {
            'session': ses,'image':image,'name':name,'subid':path[:2]
        }
    except:
        return {}