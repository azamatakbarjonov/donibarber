from django.shortcuts import render

def price_view(request):

    context = {

    }
    return render(request, 'price.html', context)