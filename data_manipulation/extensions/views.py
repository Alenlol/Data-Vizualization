from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UploadFileForm, SelectForm
from .models import Document
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .utils import Visualize


# Create your views here.
def home(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        try:
            newdoc = Document.objects.get(name=request.FILES['docfile'])
        except ObjectDoesNotExist:
            if form.is_valid():
                messages.success(request, 'Successfully uploaded')
                file = form.save(commit=False)
                file.name = request.FILES['docfile']
                file.save()
            else:
                messages.error(request, form.errors['docfile'])
        else:
            messages.error(request, "file with this name is exist")
        return redirect('home')

    context = {'form': form}

    return render(request, 'extensions/home.html', context)


def chart(request):
    chart = Visualize()
    x, y = 0, 0
    result = ""
    choices = ""
    form = SelectForm()
    if request.method == 'GET':
        form = SelectForm(request.GET)

        if form.is_valid():
            choices = form.fields['new_choice'].choices[int(request.GET.get('new_choice'))][1]

            print("ok")

    context = {'chart': result, 'form': form, 'choices': choices}
    return render(request, 'extensions/charts.html', context)