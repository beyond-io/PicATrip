from django.shortcuts import render


def homepage(request):
    return render(request, 'pickATrip_django_apps/homepage.html', {'title': 'PicATrip'})


def about(request):
    return render(request, 'pickATrip_django_apps/about.html', {'title': 'About'})
