from django import forms
from .models import Task, iom_marcas, Sucursal, OrdenFabricacionEnc, Personal, Sucursal, Estatus, Hilos
from django.utils import timezone

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
        
class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'descripcion', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Sucursal.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre
    
class OrdenFabricacionEncForm(forms.ModelForm):
    class Meta:
        model = OrdenFabricacionEnc
        fields = [
            'numero', 'fecha_orden_fabricacion', 'descripcion', 'info_adicional',
            'id_cortador', 'fecha_corte', 'fecha_armado', 'fecha_embalaje',
            'id_sucursal', 'id_estatus', 'activo',
            'id_vendedor', 'id_armador', 'id_empacador', 'id_hilos'
        ]
        widgets = {
            'fecha_orden_fabricacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_corte': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_armado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_embalaje': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'info_adicional': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los queryset para búsqueda por nombre y apellido
        for field in ['id_cortador', 'id_vendedor', 'id_armador', 'id_empacador']:
            self.fields[field].queryset = Personal.objects.order_by('nombre', 'apellido_paterno')
            self.fields[field].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido_paterno}"
            self.fields[field].widget.attrs.update({'class': 'form-select'})
        self.fields['id_sucursal'].queryset = Sucursal.objects.order_by('nombre')
        self.fields['id_sucursal'].widget.attrs.update({'class': 'form-select'})
        self.fields['id_estatus'].queryset = Estatus.objects.order_by('nombre')
        self.fields['id_estatus'].widget.attrs.update({'class': 'form-select'})
        self.fields['id_hilos'].queryset = Hilos.objects.order_by('nombre')
        self.fields['id_hilos'].widget.attrs.update({'class': 'form-select'})       
 