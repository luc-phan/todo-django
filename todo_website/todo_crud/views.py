from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from .models import Todo
from .forms import TodoForm, TodoFormSet

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'todo_crud/index.html'

    def get_queryset(self):
        return Todo.objects.all().order_by('done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodoForm()
        context['formset'] = TodoFormSet(queryset=self.object_list)
        return context

    def post(self, *args, **kwargs):
        formset = TodoFormSet(data=self.request.POST)

        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("index"))

        raise ValidationError(formset.errors)
