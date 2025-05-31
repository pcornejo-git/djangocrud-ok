from django import forms
from .models import Task, Marcas, Sucursal, OrdenFabricacionEnc, Personal, Sucursal, Estatus, Hilos, Proposito, Modelos
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

class PropositoForm(forms.ModelForm):
    class Meta:
        model = Proposito
        fields = ['nombre', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Proposito.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['nombre', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Marcas.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

class EstatusForm(forms.ModelForm):
    class Meta:
        model = Estatus
        fields = ['nombre', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Marcas.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

class HilosForm(forms.ModelForm):
    class Meta:
        model = Hilos
        fields = ['nombre', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Marcas.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

class MarcasForm(forms.ModelForm):
    class Meta:
        model = Marcas
        fields = ['nombre', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Marcas.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre
        
class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre','direccion','ciudad' ,'descripcion', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Sucursal.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

class ModelosForm(forms.ModelForm):
    class Meta:
        model = Modelos
        fields = ['nombre','id_marcas','activo' ,
                  'fecha_ini', 'fecha_ter', 'num_asientos',
                  'num_filas', 'serie', 'accesorios']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'id_marcas': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_ini': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_ter': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_asientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_filas': forms.NumberInput(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'accesorios': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los queryset para búsqueda por nombre y apellido
        for field in ['id_marcas']:
            self.fields[field].queryset = Marcas.objects.order_by('nombre')
            self.fields[field].label_from_instance = lambda obj: f"{obj.nombre}"
            self.fields[field].widget.attrs.update({'class': 'form-select'})
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].upper()
        if Modelos.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre ya existe.')
        return nombre

    
class OrdenFabricacionEncForm(forms.ModelForm):
    class Meta:
        model = OrdenFabricacionEnc
        fields = [
            'numero', 'fecha_orden_fabricacion', 'descripcion', 'info_adicional',
            'id_cortador', 'fecha_corte', 'fecha_armado', 'fecha_embalaje',
            'id_sucursal', 'id_estatus', 'activo',
            'id_vendedor', 'id_armador', 'id_empacador', 'id_hilos','id_proposito'
        ]
        widgets = {
            'fecha_orden_fabricacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_corte': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_armado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_embalaje': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
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
        # Solo mostrar personas con cortador=True en el campo id_cortador
        self.fields['id_cortador'].queryset = Personal.objects.filter(cortador=True).order_by('nombre', 'apellido_paterno')
        self.fields['id_vendedor'].queryset = Personal.objects.filter(vendedor=True).order_by('nombre', 'apellido_paterno')
        self.fields['id_armador'].queryset = Personal.objects.filter(armador=True).order_by('nombre', 'apellido_paterno')   
        self.fields['id_empacador'].queryset = Personal.objects.filter(empacador=True).order_by('nombre', 'apellido_paterno')
        # ...el resto de tu lógica para otros campos...
        self.fields['id_sucursal'].queryset = Sucursal.objects.order_by('nombre')
        self.fields['id_sucursal'].widget.attrs.update({'class': 'form-select'})
        self.fields['id_estatus'].queryset = Estatus.objects.order_by('nombre')
        self.fields['id_estatus'].widget.attrs.update({'class': 'form-select'})
        self.fields['id_hilos'].queryset = Hilos.objects.order_by('nombre')
        self.fields['id_hilos'].widget.attrs.update({'class': 'form-select'})       
        self.fields['id_proposito'].queryset = Proposito.objects.order_by('nombre')
        self.fields['id_proposito'].widget.attrs.update({'class': 'form-select'})       
 