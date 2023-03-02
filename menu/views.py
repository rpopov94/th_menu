from django.shortcuts import render

def my_view(request, item=None):
    return render(request, 'index.html', {'item': item})

