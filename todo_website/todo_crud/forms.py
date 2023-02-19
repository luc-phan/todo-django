from django import forms

from .models import Todo


TodoFormSet = forms.modelformset_factory(
    Todo,
    fields=["done"],
    extra=0,
    widgets = {
        'done': forms.CheckboxInput(attrs={'class': 'form-check-input'})
    }
)


class NewTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["done", "title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={'class': "form-control"}),
            "description": forms.Textarea(attrs={'class': "form-control"})
        }
