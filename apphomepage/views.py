from django.shortcuts import render


def homepage(request):
    return render(request, 'apphomepage/homepage.html')


def about(request):
    return render(request, 'apphomepage/about.html')
