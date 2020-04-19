from django.shortcuts import render

# Create your views here.

def teacher(request):
    if request.method == "POST":
        print('rahul')
        name=request.POST.get('name')
        number=request.POST.get('number')
        email=request.POST.get('email')
        age=request.POST.get('age')
        experience=request.POST.get('experience')
        gen=request.POST.get('gen')
        s=request.POST.get('s')
        d=request.POST.get('d')
        print(name,number,email,age,experience,gen,s,d)
        
        if(name==''):
            error="Name is invalid"
            data = {
                'name':name,
                'number':number,
                'email':email,
                'age':age,
                'experience':experience,
                'gen':gen,
                's':s,
                'd':d,
                'error':error
            }
            return render(request,'teacher.html',data)
        data = {
                'name':name,
                'number':number,
                'email':email,
                'age':age,
                'experience':experience,
                'gen':gen,
                's':s,
                'd':d,
        }
        return render(request,'teacher.html',data)
    else:    
        name=""
        print('rahul11')
        email=""
        data = {
            'name':name,
            'email':email,
            's':'Select State First',
            'error': '',
            'success': '',
            'info': ''
        }
        return render(request,'teacher.html',data)
