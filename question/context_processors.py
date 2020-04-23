def add_variable_to_context(request):
    ses = request.session['us']
    return {
        'session': ses
    }