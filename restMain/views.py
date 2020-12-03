from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def IndexMain(request):
    return redirect('CustomerAndDish/')
    # return render(request,'index.html')


def IndexAbout(request):
    return render(request,'About_developer.html')