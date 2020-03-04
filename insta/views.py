from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required(login_url='/accounts/login/')
def home(request):
    images = Image.objects.all()
    return render(request, 'insta/index.html',{"images":images})

