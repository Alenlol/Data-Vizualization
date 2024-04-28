from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import UploadFileForm, SelectForm, SelectColumnForm, SelectColumnFormY
from .models import Document
from django.core.exceptions import ObjectDoesNotExist
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
    new_forms = ""
    choices = ""
    form = ""
    if request.method == 'GET':
        form = SelectForm(request.GET, values=Document.objects.values_list('name'))

        if form.is_valid():
            choices = form.fields['new_choice'].choices[int(request.GET.get('new_choice'))][1]
            return redirect('chart_by', choices[:-4])

    context = {'new_forms': new_forms, 'form': form, 'choices': choices}
    return render(request, 'extensions/files.html', context)


class ChartUpdate(TemplateView):
    template_name = 'extensions/charts.html'

    def get(self, request, *args, **kwargs):
        chart = ""
        data = Visualize(kwargs['pk'] + ".csv")
        title_names = data.get_title_names()
        title_by_index = [(i, j) for i, j in enumerate(title_names)]
        extra_indexies = len(request.GET)-2
        title_formX = SelectColumnForm(request.GET, extra=extra_indexies-1, values=title_by_index)
        title_formY = SelectColumnFormY(request.GET, values=title_by_index)

        if request.GET.get('form_type') == 'pop':
            title_formX = SelectColumnForm(request.GET, extra=extra_indexies-2, values=title_by_index)
        if request.GET.get('form_type') == "change-data":
            print('change-data')
        if extra_indexies >= len(title_by_index)-1:
            extra_indexies -= 1
        if request.GET.get('form_type') == 'add-title':
            print('add-title')
            title_formX = SelectColumnForm(request.GET, extra=extra_indexies, values=title_by_index)
        if request.GET.get('form_type') == 'send':
            print('send')
            submitted_values = []
            for value in request.GET:
                index = request.GET.get(value)
                if index.isdigit():
                    submitted_values.append(title_names[int(index)])

            if data.check_data(submitted_values):
                chart = data.get_plot(x=submitted_values[0], y=submitted_values[-1])

        context = {'title_formX': title_formX, 'title_formY': title_formY, 'chart': chart}
        return self.render_to_response(context)

