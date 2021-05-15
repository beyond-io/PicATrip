from django.shortcuts import render, redirect


def homepage(request):
    return redirect('view posts', permanent=True)


def about(request):
    return render(request, 'pickATrip_django_apps/about.html', {'title': 'About'})
