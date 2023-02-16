from django.views import generic

from .models import Todo

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'todo_crud/index.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.all()
