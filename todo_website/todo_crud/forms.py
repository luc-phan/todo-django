from django import forms

from .models import Todo


class IndexTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["done", "title"]


TodoFormSet = forms.modelformset_factory(Todo, fields=["done"], extra=0)


class NewTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["done", "title", "description"]
        widgets = {
            "description": forms.Textarea()
        }
