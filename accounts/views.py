from django.http import HttpResponse
from django.template import loader
from accounts.models import User

#Https
def user_list(request):
    user = User.objects.all()
    template = loader.get_template('accounts/user_list.html')
    context = {"user": user}
    output = template.render(context, request)
    return HttpResponse(output)



