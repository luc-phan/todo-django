import logging
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from .models import Todo
from .forms import TodoFormSet, NewTodoForm

_logger = logging.getLogger(__name__)

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'todo_crud/index.html'

    def get_queryset(self):
        return Todo.objects.all().order_by('done', '-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = TodoFormSet(queryset=self.object_list)
        return context

    def post(self, *args, **kwargs):
        formset = TodoFormSet(data=self.request.POST)

        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("index"))

        _logger.error("non_form_errors = %s", formset.non_form_errors())
        raise ValidationError(formset.errors)


class DetailView(generic.DetailView):
    model = Todo
    template_name = 'todo_crud/detail.html'


class CreateView(generic.edit.CreateView):
    model = Todo
    form_class = NewTodoForm
    success_url = reverse_lazy("index")
