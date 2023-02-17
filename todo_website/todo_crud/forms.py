from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["done", "title"]

TodoFormSet = forms.modelformset_factory(Todo, fields=["done"], extra=0)
