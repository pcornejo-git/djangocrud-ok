from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task, Marcas, Sucursal, OrdenFabricacionEnc, Proposito,  Personal, Estatus, Hilos

from .forms import TaskForm, MarcasForm, SucursalForm, OrdenFabricacionEncForm, PropositoForm, PersonalForm, EstatusForm, HilosForm
from django.db.models import Q
import barcode
from barcode.writer import ImageWriter
import io
import base64
import csv
from django.http import HttpResponse

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def marcas_list(request):
    marcas = Marcas.objects.all()
    nombre = request.GET.get('nombre', '')
    activo = request.GET.get('activo', '')
    sort = request.GET.get('sort', '')
    if nombre:
        marcas = marcas.filter(nombre__icontains=nombre)
    if activo:
        marcas = marcas.filter(activo__icontains=activo)
    if sort:
        marcas = marcas.order_by(sort)
    else:
        marcas = marcas.order_by('nombre')

    # Exportar a CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="marcas.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Activo',])
        for m in marcas:
            writer.writerow([m.nombre, m.activo])
        return response

    context = {
        'marcas': marcas,
        'activo': activo,
    }
    return render(request, 'marcas_list.html', context)

@login_required
def marcas_create(request):
    if request.method == 'POST':
        form = MarcasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marcas_list')
    else:
        form = MarcasForm()
    return render(request, 'marcas_form.html', {'form': form})

@login_required
def marcas_update(request, pk):
    marcas = get_object_or_404(Marcas, pk=pk)
    if request.method == 'POST':
        form = MarcasForm(request.POST, instance=marcas)
        if form.is_valid():
            form.save()
            return redirect('marcas_list')
    else:
        form = MarcasForm(instance=marcas)
    return render(request, 'marcas_form.html', {'form': form})


@login_required
def marcas_delete(request, pk):
    marcas = get_object_or_404(Marcas, pk=pk)
    if request.method == 'POST':
        marcas.delete()
        return redirect('marcas_list')
    return render(request, 'marcas_confirm_delete.html', {'marcas': marcas})


@login_required
def sucursal_list(request):
    sucursales = Sucursal.objects.all()
    nombre = request.GET.get('nombre', '')
    direccion = request.GET.get('direccion', '')
    ciudad = request.GET.get('ciudad', '')
    activo = request.GET.get('activo', '')
    descripcion = request.GET.get('descripcion', '')
    sort = request.GET.get('sort', '')
    if nombre:
        sucursales = sucursales.filter(nombre__icontains=nombre)
    if direccion:
        sucursales = sucursales.filter(direccion__icontains=direccion)
    if ciudad:
        sucursales = sucursales.filter(ciudad__icontains=ciudad)
    if descripcion:
        sucursales = sucursales.filter(descripcion__icontains=descripcion)  
    if activo:
        sucursales = sucursales.filter(activo__icontains=activo)
    if sort:
        sucursales = sucursales.order_by(sort)
    else:
        sucursales = sucursales.order_by('nombre')

    # Exportar a CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sucursales.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Direccion', 'Ciudad','Descripcion','Activo',])
        for s in sucursales:
            writer.writerow([s.nombre, s.direccion, s.ciudad, s.descripcion,s.activo])
        return response

    context = {
        'sucursales': sucursales,
        'nombre': nombre,
        'direccion': direccion,
        'ciudad': ciudad,
        'descripcion': descripcion,
        'activo': activo,
    }
    return render(request, 'sucursal_list.html', context)

@login_required
def sucursal_create(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucursal_list')
    else:
        form = SucursalForm()
    return render(request, 'sucursal_form.html', {'form': form})

@login_required
def sucursal_update(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('sucursal_list')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'sucursal_form.html', {'form': form})

@login_required
def sucursal_delete(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('sucursal_list')
    return render(request, 'sucursal_confirm_delete.html', {'sucursal': sucursal})

@login_required
def orden_list(request):
#    query = request.GET.get('q', '')
    ordenes = OrdenFabricacionEnc.objects.all()
#    if query:
#        ordenes = ordenes.filter(
#            Q(id_cortador__nombre__icontains=query) |
#            Q(id_cortador__apellido_paterno_icontains=query) |
#            Q(id_vendedor__nombre__icontains=query) |
#            Q(id_vendedor__apellido_paterno_icontains=query) |
#            Q(id_armador__nombre__icontains=query) |
#            Q(id_armador__apellido_paterno_icontains=query) |
#            Q(id_empacador__nombre__icontains=query) |
#            Q(id_empacador__apellido_paterno_icontains=query) |
#            Q(id_sucursal__nombre__icontains=query) |
#            Q(id_estatus__nombre__icontains=query) |
#            Q(id_hilos__nombre__icontains=query)
#        )
#    return render(request, 'orden_list.html', {'ordenes': ordenes, 'query': query})

    numero = request.GET.get('numero', '')
    descripcion = request.GET.get('descripcion', '')
    cortador = request.GET.get('cortador', '')
    sucursal = request.GET.get('sucursal', '')
    estatus = request.GET.get('estatus', '')
    vendedor = request.GET.get('vendedor', '')
    armador = request.GET.get('armador', '')
    empacador = request.GET.get('empacador', '')
    hilos = request.GET.get('hilos', '')
    proposito = request.GET.get('proposito', '')

    sort = request.GET.get('sort')
    if sort:
        ordenes = ordenes.order_by(sort)
    else:
        ordenes = ordenes.order_by('-numero')  # Ordena por defecto por 'numero' descendente    
    if numero:
        ordenes = ordenes.filter(numero=numero)
    if descripcion:
        ordenes = ordenes.filter(descripcion__icontains=descripcion)
    if cortador:
        ordenes = ordenes.filter(id_cortador__nombre__icontains=cortador)
    if sucursal:
        ordenes = ordenes.filter(id_sucursal__nombre__icontains=sucursal)
    if estatus:
        ordenes = ordenes.filter(id_estatus__nombre__icontains=estatus)
    if vendedor:
        ordenes = ordenes.filter(id_vendedor__nombre__icontains=vendedor)
    if armador:
        ordenes = ordenes.filter(id_armador__nombre__icontains=armador)
    if empacador:
        ordenes = ordenes.filter(id_empacador__nombre__icontains=empacador)
    if hilos:
        ordenes = ordenes.filter(id_hilos__nombre__icontains=hilos)
    if proposito:
        ordenes = ordenes.filter(id_hilos__nombre__icontains=proposito)

    context = {
        'ordenes': ordenes,
        'numero': numero,
        'descripcion': descripcion,
        'cortador': cortador,
        'sucursal': sucursal,
        'estatus': estatus,
        'vendedor': vendedor,
        'armador': armador,
        'empacador': empacador,
        'hilos': hilos,
        'proposito': proposito,}
    # Exportar a CSV si se presionó el botón
    if request.GET.get('export') == 'csv' or request.POST.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ordenes.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Numero', 'Fecha Orden', 'Descripcion', 'Cortador', 'Sucursal', 'Estatus',
            'Vendedor', 'Armador', 'Empacador', 'Hilos','Proposito', 'Activo'
        ])
        for orden in ordenes:
            writer.writerow([
                orden.numero,
                orden.fecha_orden_fabricacion.strftime('%d/%m/%Y') if orden.fecha_orden_fabricacion else '',
                orden.descripcion,
                str(orden.id_cortador),
                str(orden.id_sucursal),
                str(orden.id_estatus),
                str(orden.id_vendedor),
                str(orden.id_armador),
                str(orden.id_empacador),
                str(orden.id_hilos),
                str(orden.id_proposito),
                'Sí' if orden.activo else 'No'
            ])
        return response

    # ... tu render habitual ...
    return render(request, 'orden_list.html', context)

@login_required
def orden_create(request):
    if request.method == 'POST':
        form = OrdenFabricacionEncForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orden_list')
    else:
        form = OrdenFabricacionEncForm()
    return render(request, 'orden_form.html', {'form': form})

@login_required
def orden_update(request, pk):
    orden = get_object_or_404(OrdenFabricacionEnc, pk=pk)
    if request.method == 'POST':
        form = OrdenFabricacionEncForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('orden_list')
    else:
        form = OrdenFabricacionEncForm(instance=orden)
    return render(request, 'orden_form.html', {'form': form})

@login_required
def orden_delete(request, pk):
    orden = get_object_or_404(OrdenFabricacionEnc, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('orden_list')
    return render(request, 'orden_confirm_delete.html', {'orden': orden})


@login_required
def orden_print(request, pk):
    orden = get_object_or_404(OrdenFabricacionEnc, pk=pk)
    # Generar código de barras en memoria
    buffer = io.BytesIO()
    barcode_class = barcode.get_barcode_class('code128')
    barcode_img = barcode_class(str(orden.numero), writer=ImageWriter())
    barcode_img.write(buffer)
    barcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return render(request, 'orden_print.html', {'orden': orden, 'barcode_base64': barcode_base64})
