from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImportantClassifiersForm

# Create your views here.
def index(request):
    form = ImportantClassifiersForm(request.POST)
    template_name = 'ask_for_input.html'
    context = {
    'form':form
    }
    print(template_name)
    return render(request, template_name, context)

def show_result(request):
    print("inside show_result")
    template_name = 'show_result.html'
    result = request.POST.get('first_classifier')
    context = {
    'result':result
    }
    print(result)
    return render(request, template_name, context)
