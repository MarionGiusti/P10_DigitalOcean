from django.shortcuts import render, redirect



def results(request):
    context = {}
    return render(request, 'catalogue/results.html', context)
