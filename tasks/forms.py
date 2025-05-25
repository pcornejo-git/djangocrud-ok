from django import forms
from .models import Task, iom_marcas


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el titulo'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Escriba la descripcion'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }

class MarcaForm(forms.ModelForm):
    class Meta:
        model = iom_marcas
        fields = ['nombre', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }