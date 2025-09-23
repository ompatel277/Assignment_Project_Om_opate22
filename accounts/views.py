from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from accounts.models import User

#Https
def user_list_http(request):
    user = User.objects.all()
    template = loader.get_template('accounts/user_list.html')
    context = {"user": user}
    output = template.render(context, request)
    return HttpResponse(output)

# render
def user_list_render(request):
    user = User.objects.all()
    return render(request, 'accounts/user_list.html', {'user': user})


