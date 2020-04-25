def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        path=request.path
        print(path)
        if 'id' in path:
            print(path)
        return {
            'session': ses,'image':image,'name':name,'path':path
        }
    except:
        return {}