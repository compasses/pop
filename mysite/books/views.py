from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def search_form(request):
    return render(request, "books/search_form.html")

def search(request):
    if 'q' in request.GET:
        message = 'You search for : %r' % request.GET['q']
    else:
        message = 'You sumbit an empty search'
    return HttpResponse(message)
