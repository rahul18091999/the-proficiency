from django.shortcuts import render
from exam.views import database
# Create your views here.

def viewNotifications(request):
    return render(request,'./notification/viewNotifications.html')


def addNotifications(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('discription')
        to = request.POST.get('to')
        print(to)
        data = database.child(to).get().val()
        token=[]
        # print(data)
        if data:
            for j in data:
                if 'notifications' in data[j]:
                    token.append(data[j]['notifications']['token'])
        print(token)
        import requests
        r = requests.post('https://exp.host/--/api/v2/push/send',
        headers={
            "HTTP_ACCEPT":'application/json',
            "HTTP_ACCEPT_ENCODING":'gzip, deflate',
            "HTTP_HOST":'the-proficiency.com',
            'Content-type': 'application/json'
        },
        json={
            'to':token,                        
              'title': title,                  
              'body': desc,             
              'priority': "high",            
              'sound':"default",              
              'channelId':"default",   

        })
        print(r.text)
#         fetch('https://exp.host/--/api/v2/push/send', {       
#          method: 'POST', 
#          headers: {
#                Accept: 'application/json',  
#               'Content-Type': 'application/json', 
#               'accept-encoding': 'gzip, deflate',   
#               'host': 'exp.host'      
#           }, 
#         body: JSON.stringify({                 
#               to: token,                        
#               title: 'New Notification',                  
#               body: 'The notification worked!',             
#               priority: "high",            
#               sound:"default",              
#               channelId:"default",   
#                   }),        
#       }).then((response) => response.json())   
#                .then((responseJson) => {  })
#                       .catch((error) => { console.log(error) });
# }
    return render(request,'./notification/addNotifications.html')


    