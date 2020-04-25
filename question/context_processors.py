def add_variable_to_context(request):
    try:
        path=request.GET.get('id')
    except:
        path='999'
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        
<<<<<<< HEAD
        if(request.path.find('id')):
            path=request.GET.get('id')
        else:
            path='999'
        return {
            'session': ses,'image':image,'name':name,'subid':path
=======
        
        try:
            path=request.GET.get('id')
            return {
                'session': ses,'image':image,'name':name,'subid':path[:2]
            }
        except:
            return {
                'session': ses,'image':image,'name':name,'subid':path[:2]
>>>>>>> 2f7100d75fb7a58d2c7d50b61ec728e755517f7e
            }
    except:
        return {}