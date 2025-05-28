from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task, iom_marcas, Sucursal, OrdenFabricacionEnc

from .forms import TaskForm, MarcaForm, SucursalForm,  OrdenFabricacionEncForm
from django.db.models import Q
import barcode
from barcode.writer import ImageWriter
import io
import base64

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
def marcas(request):
    marcas = iom_marcas.objects.all().order_by('id_marcas')
    if request.method == 'POST':
        if 'id' in request.POST:
            marca = get_object_or_404(iom_marcas, pk=request.POST['id'])
            form = MarcaForm(request.POST, instance=marca)
        else:
            form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marcas')
    else:
        form = MarcaForm()
    return render(request, 'marcas.html', {'marcas': marcas, 'form': form})

@login_required
def editar_marca(request, id_marcas):
    marca = get_object_or_404(iom_marcas, pk=id_marcas)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('marcas')
    else:
        form = MarcaForm(instance=marca)
    marcas = iom_marcas.objects.all().order_by('id_marcas')
    return render(request, 'marcas.html', {'marcas': marcas, 'form': form})

@login_required
def eliminar_marca(request, id_marcas):
    marca = get_object_or_404(iom_marcas, pk=id_marcas)
    if request.method == 'POST':
        marca.delete()
        return redirect('marcas')
    return render(request, 'confirmar_eliminar.html', {'marca': marca})

@login_required
def sucursal_list(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sucursal_list.html', {'sucursales': sucursales})

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

    sort = request.GET.get('sort')
    if sort:
        ordenes = ordenes.order_by(sort)
    else:
        ordenes = ordenes.order_by('-numero')  # Ordena por defecto por 'numero'    
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
    }
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
