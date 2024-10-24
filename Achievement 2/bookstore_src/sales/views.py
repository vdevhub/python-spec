from django.shortcuts import render

# to protect function-based views
from django.contrib.auth.decorators import login_required

from .forms import SalesSearchForm


# Create your views here.
def home(request):
    return render(request, "sales/home.html")


# define function-based view - records(records()
# keep protected
@login_required
def records(request):
    # create an instance of SalesSearchForm that you defined in sales/forms.py
    form = SalesSearchForm(request.POST or None)

    # pack up data to be sent to template in the context dictionary
    context = {
        "form": form,
    }

    # load the sales/record.html page using the data that you just prepared
    return render(request, "sales/records.html", context)
