def add_variable_to_context(request):
    try:
        ses = request.session['us']
        image=request.session['image']
        name=request.session['name']
        
        
        try:
            path=request.GET.get('id')
<<<<<<< HEAD
            return {
                'session': ses,'image':image,'name':name,'subid':path[:2]
=======
        else:
            path='999'
        return {
            'session': ses,'homeimage':image,'homename':name,'subid':str(path)[:2]
>>>>>>> fb176d3e064a86fbd1aa3c2a74719a303053c323
            }
        except:
            pass
        return {
            'session': ses,'image':image,'name':name
        }
    except:
        return {}
