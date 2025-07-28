from django.shortcuts import render

def navi_view(request):
    
    context = {

    }
    return render(request, 'navigate.html', context)