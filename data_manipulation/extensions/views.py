from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Document


# Create your views here.
def home(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['file'])
            newdoc.save()

            messages.success(request, 'Successfully uploaded')

            print(1)
        else:
            print(0)
        return redirect('home')

    context = {'form': form}

    return render(request, 'extensions/home.html', context)

