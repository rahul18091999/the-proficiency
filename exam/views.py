from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import pyrebase
config={
    'apiKey': "AIzaSyBvVgen1TvuoKinJYwvaNH8n7VIACGbqgI",
    'authDomain': "the-proficiency.firebaseapp.com",
    'databaseURL': "https://the-proficiency.firebaseio.com",
    'projectId': "the-proficiency",
    'storageBucket': "the-proficiency.appspot.com",
    'messagingSenderId': "859931947137",
    'appId': "1:859931947137:web:66edfbcbe4489fab789d80"
}
firebase=pyrebase.initialize_app(config);
auth = firebase.auth()
database=firebase.database()

def header(request):
    return render(request,'admin.html')



def addTeacher(request):
    name=request.GET.get('name')
    return render('/teacher',{'name':name})