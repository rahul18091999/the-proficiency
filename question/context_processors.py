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
<<<<<<< HEAD
            pass
        return {
            'session': ses,'image':image,'name':name
        }
=======
            return {
                'session': ses,'image':image,'name':name,'subid':path[:2]
>>>>>>> 2f7100d75fb7a58d2c7d50b61ec728e755517f7e
            }
>>>>>>> 1dd0ab8e753f249657d9d6c909cdbcb3e42cad9c
    except:
        return {}