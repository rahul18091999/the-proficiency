def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        
        if(request.path.find('id')):
            path=request.GET.get('id')
        else:
            path='999'
        return {
            'session': ses,'image':image,'name':name,'subid':path
            }
    except:
        return {}
