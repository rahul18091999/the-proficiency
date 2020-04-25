def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        return {
            'session': ses,'image':image,'name':name
        }
    except:
        return {}