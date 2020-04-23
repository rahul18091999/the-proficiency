def add_variable_to_context(request):
    try:
        ses = request.session['us']
        return {
            'session': ses
        }
    except:
        return {}