def add_variable_to_context(request):
    try:
        path=request.GET.get('id')
    except:
        path='999'