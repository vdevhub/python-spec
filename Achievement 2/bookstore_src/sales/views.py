from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "sales/home.html")


# define function-based view - records(records()
def records(request):
    # do nothing, simply display page
    return render(request, "sales/records.html")
