from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import UploadFileForm, SelectForm, SelectColumnForm, SelectColumnFormY
from .models import Document
from django.core.exceptions import ObjectDoesNotExist
from .utils import Visualize


# Create your views here.
class Home(TemplateView):
    template_name = 'extensions/home.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        context = {'form': form}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        try:
            Document.objects.get(name=request.FILES['docfile'])
        except ObjectDoesNotExist:
            if form.is_valid():
                messages.success(request, 'Successfully uploaded')
                file = form.save(commit=False)
                file.name = request.FILES['docfile']
                file.save()
                return redirect('home')
            else:
                messages.error(request, form.errors['docfile'])
        else:
            messages.error(request, "file with this name is exist")

        return redirect('home')


class FileChoose(TemplateView):
    template_name = 'extensions/files.html'

    def get(self, request, *args, **kwargs):
        choices = ""

        form = SelectForm(request.GET, values=Document.objects.values_list('name'))

        if form.is_valid():
            choices = form.fields['new_choice'].choices[int(request.GET.get('new_choice'))][1]
            return redirect('files_by', choices[:-4])

        context = {'form': form, 'choices': choices}
        return self.render_to_response(context)


class ChartUpdate(TemplateView):
    template_name = 'extensions/charts.html'

    def get_charts(self, request, data):
        title_names = data.get_title_names()
        submitted_values = []
        for value in request.GET:
            index = request.GET.get(value)
            if index.isdigit():
                submitted_values.append(title_names[int(index)])

        if data.check_data(submitted_values):
            return [data.get_plot(x=submitted_values[0], y=submitted_values[-1], plot_type='plot'),
                    data.get_plot(x=submitted_values[0], y=submitted_values[-1], plot_type='scatter'),
                    data.get_plot(x=submitted_values[0], y=submitted_values[-1], plot_type='bar'),]
        else:
            messages.error(request, 'cannot two or more similar table names')

    def get(self, request, *args, **kwargs):
        charts = ""
        data = Visualize(kwargs['pk'] + ".csv")
        title_by_index = [(i, j) for i, j in enumerate(data.get_title_names())]
        extra_indexies = len(request.GET)-2
        title_formX = SelectColumnForm(request.GET, extra=extra_indexies-1, values=title_by_index)
        title_formY = SelectColumnFormY(request.GET, values=title_by_index)

        if request.GET.get('form_type') == 'pop':
            title_formX = SelectColumnForm(request.GET, extra=extra_indexies-2, values=title_by_index)
        if extra_indexies >= len(title_by_index)-1:
            extra_indexies -= 1
        if request.GET.get('form_type') == 'add-title':
            title_formX = SelectColumnForm(request.GET, extra=extra_indexies, values=title_by_index)
        if request.GET.get('form_type') == 'show':
            charts = self.get_charts(request, data)

        context = {'title_formX': title_formX, 'title_formY': title_formY, 'charts': charts}
        return self.render_to_response(context)

