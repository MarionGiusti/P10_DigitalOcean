from django.shortcuts import render, redirect



def search(request):
    context = {}
    return render(request, 'catalogue/results.html', context)
