def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        
        
        try:
            ses = request.session['us']
            image=request.session['image']
            name=request.session['name']
            path=request.GET.get('id')
            return {
            'session': ses,'image':image,'name':name,'subid':path[:2]
            }
        except:
            pass
        # return {
        #     'session': ses,'image':image,'name':name,'subid':path[:2]
        # }
    except:
        return {}