from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task, Marcas, Sucursal, OrdenFabricacionEnc, Proposito,  Personal, Estatus, Hilos, Modelos

from .forms import TaskForm, MarcasForm, SucursalForm, OrdenFabricacionEncForm, PropositoForm, PersonalForm, EstatusForm, HilosForm, ModelosForm
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
def hilos_list(request):
    hilos = Hilos.objects.all()
    nombre = request.GET.get('nombre', '')
    color = request.GET.get('color', '')
    descripcion = request.GET.get('descripcion', '')
    activo = request.GET.get('activo', '')
    sort = request.GET.get('sort', '')
    if nombre:
        hilos = hilos.filter(nombre__icontains=nombre)
    if color:
        hilos = hilos.filter(activo__icontains=color)
    if descripcion:
        hilos = hilos.filter(activo__icontains=descripcion)
    if activo:
        hilos = hilos.filter(activo__icontains=activo)
    if sort:
        hilos = hilos.order_by(sort)
    else:
        hilos = hilos.order_by('nombre')

    # Exportar a CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="hilos.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Color', 'Descripcion', 'Activo',])
        for h in hilos:
            writer.writerow([h.nombre, h.color, h.descripcion, h.activo])
        return response

    context = {
        'hilos': hilos,
        'nombre': nombre,
        'color': color,
        'descripcion': descripcion,
        'activo': activo,
    }
    return render(request, 'hilos_list.html', context)

@login_required
def hilos_create(request):
    if request.method == 'POST':
        form = HilosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hilos_list')
    else:
        form = HilosForm()
    return render(request, 'hilos_form.html', {'form': form})

@login_required
def hilos_update(request, pk):
    hilos = get_object_or_404(Hilos, pk=pk)
    if request.method == 'POST':
        form = HilosForm(request.POST, instance=hilos)
        if form.is_valid():
            form.save()
            return redirect('hilos_list')
    else:
        form = HilosForm(instance=hilos)
    return render(request, 'hilos_form.html', {'form': form})


@login_required
def hilos_delete(request, pk):
    hilos = get_object_or_404(hilos, pk=pk)
    if request.method == 'POST':
        hilos.delete()
        return redirect('hilos_list')
    return render(request, 'hilos_confirm_delete.html', {'hilos': hilos})

@login_required
def personal_list(request):
    personal = Personal.objects.all()
    nickname = request.GET.get('nickname', '')
    nombre = request.GET.get('nombre', '')
    apellido_paterno = request.GET.get('apellido_paterno', '')
    apellido_materno = request.GET.get('apellido_materno', '')
    fecha_nacimiento = request.GET.get('fecha_nacimiento', '')
    vendedor = request.GET.get('vendedor', '')
    armador = request.GET.get('armador', '')
    empacador = request.GET.get('empacador', '')
    cortador = request.GET.get('cortador', '')
    activo = request.GET.get('activo', '')
    sort = request.GET.get('sort', '')
    if nickname:
        personal = personal.filter(nombre__icontains=nickname)
    if nombre:
        personal = personal.filter(nombre__icontains=nombre)
    if apellido_paterno:
        personal = personal.filter(activo__icontains=apellido_paterno)
    if apellido_materno:
        personal = personal.filter(activo__icontains=apellido_materno)
    if fecha_nacimiento:
        personal = personal.filter(activo__icontains=fecha_nacimiento)
    if vendedor:
        personal = personal.filter(activo__icontains=vendedor)
    if armador:
        personal = personal.filter(activo__icontains=armador)
    if empacador:
        personal = personal.filter(activo__icontains=empacador)
    if cortador:
        personal = personal.filter(activo__icontains=cortador)
    if activo:
        personal = personal.filter(activo__icontains=activo)
    if sort:
        personal = personal.order_by(sort)
    else:
        personal = personal.order_by('nombre')

    # Exportar a CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Personal.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Nickname', 'Apellido_paterno', 'Apellido_materno', 'Fecha_nacimiento', 'Vendedor', 'Armador', 'Empacador', 'Cortador', 'Activo',])
        for p in personal:
            writer.writerow([p.nombre, p.nickname, p.apellido_paterno, p.apellido_materno, p.fecha_nacimiento, p.vendedor, p.armador, p.empacador, p.cortador, p.activo])
        return response

    context = {
        'personal': personal,
        'nombre': nombre,
        'nickname': nickname,
        'apellido_paterno': apellido_paterno,
        'apellido_materno': apellido_materno,
        'fecha_nacimiento': fecha_nacimiento,
        'vendedor': vendedor,
        'armador': armador,
        'empacador': empacador,
        'cortador': cortador,
        'activo': activo,
    }
    return render(request, 'personal_list.html', context)

@login_required
def personal_create(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = PersonalForm()
    return render(request, 'personal_form.html', {'form': form})

@login_required
def personal_update(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = PersonalForm(instance=personal)
    return render(request, 'personal_form.html', {'form': form})


@login_required
def personal_delete(request, pk):
    personal = get_object_or_404(personal, pk=pk)
    if request.method == 'POST':
        personal.delete()
        return redirect('personal_list')
    return render(request, 'personal_confirm_delete.html', {'personal': personal})

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
def modelos_list(request):
    modelos = Modelos.objects.all()
    nombre = request.GET.get('nombre', '')
    marcas = request.GET.get('marcas', '')
    activo = request.GET.get('activo', '')
    fecha_ini = request.GET.get('fecha_ini', '')
    fecha_ter = request.GET.get('fecha_ter', '')
    num_asientos = request.GET.get('num_asientos', '')
    num_filas = request.GET.get('num_filas', '')
    serie = request.GET.get('serie', '')
    accesorios = request.GET.get('accesorios', '')
    sort = request.GET.get('sort')

    if nombre:
        modelos = modelos.filter(nombre__icontains=nombre)
    if marcas:
        modelos = modelos.filter(id_marcas__nombre__icontains=marcas)
    if num_asientos:
        modelos = modelos.filter(num_asientos__icontains=num_asientos)
    if num_filas:
        modelos = modelos.filter(num_filas__icontains=num_filas)  
    if serie:
        modelos = modelos.filter(serie__icontains=num_filas)  
    if accesorios:
        modelos = modelos.filter(accesorios__icontains=accesorios)
    if activo:
        modelos = modelos.filter(activo__icontains=activo)
        
        
    if sort:
        modelos = modelos.order_by(sort)
    else:
        modelos = modelos.order_by('nombre')

    context = {
        'modelos': modelos,
        'nombre': nombre,
        'marcas': marcas,
        'fecha_ini': fecha_ini,
        'fecha_ter': fecha_ter,
        'num_asientos': num_asientos,
        'num_filas': num_filas,
        'serie': serie,
        'accesorios': accesorios,
        }


    # Exportar a CSV si se presionó el botón
    if request.GET.get('export') == 'csv' or request.POST.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="modelos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Nombre', 'Marcas', 'Fecha_ini','Fecha_ter', 'num_asientos', 'num_filas', 'Serie',
            'Accesorios', 'Activo'
        ])

    #    print(modelos)  # Esto mostrará el queryset (no los datos)
    #    print(list(modelos))  # Esto mostrará la lista de objetos
    #    for modelo in modelos:
    #        print(modelo.nombre, modelo.id_marcas, modelo.activo)  # Muestra campos específicos
        for modelo in modelos:
            writer.writerow([
                modelo.nombre,
                str(modelo.id_marcas),
                modelo.fecha_ini,
                modelo.fecha_ter,
                modelo.num_asientos,
                modelo.num_filas,
                modelo.serie,
                modelo.accesorios,
                'Sí' if modelo.activo else 'No'
            ])
            
            
        return response
    # ... tu render habitual ...
    return render(request, 'modelos_list.html', context)

@login_required
def modelos_create(request):
    if request.method == 'POST':
        form = ModelosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modelos_list')
    else:
        form = ModelosForm()
    return render(request, 'modelos_form.html', {'form': form})

@login_required
def modelos_update(request, pk):
    modelos = get_object_or_404(Modelos, pk=pk)
    if request.method == 'POST':
        form = ModelosForm(request.POST, instance=modelos)
        if form.is_valid():
            form.save()
            return redirect('modelos_list')
    else:
        form = ModelosForm(instance=modelos)
    return render(request, 'modelos_form.html', {'form': form})

@login_required
def modelos_delete(request, pk):
    modelos = get_object_or_404(Modelos, pk=pk)
    if request.method == 'POST':
        Modelos.delete()
        return redirect('modelos_list')
    return render(request, 'modelos_confirm_delete.html', {'modelos': modelos})

@login_required
def modelos_print(request, pk):
    modelos = get_object_or_404(Modelos, pk=pk)
    if request.method == 'POST':
        Modelos.delete()
        return redirect('modelos_list')
    return render(request, 'modelos_print.html', {'modelos': modelos})


@login_required
def orden_list(request):
    ordenes = OrdenFabricacionEnc.objects.all()
    numero = request.GET.get('numero', '')
    modelo = request.GET.get('modelo', '')
    descripcion = request.GET.get('descripcion', '')
    info_adicional = request.GET.get('info_adicional', '')
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
    if modelo:
        ordenes = ordenes.filter(id_modelo__nombre__icontains=modelo)
    if descripcion:
        ordenes = ordenes.filter(descripcion__icontains=descripcion)
    if info_adicional:
        ordenes = ordenes.filter(info_adicional__icontains=info_adicional)
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
        ordenes = ordenes.filter(id_proposito__nombre__icontains=proposito)

    context = {
        'ordenes': ordenes,
        'numero': numero,
        'modelo': modelo,
        'descripcion': descripcion,
        'info_adicional': info_adicional,
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
            'Numero', 'Fecha Orden', 'Modelo','Descripcion','Info_adicional', 'Cortador', 'Sucursal', 'Estatus',
            'Vendedor', 'Armador', 'Empacador', 'Hilos','Proposito', 'Activo'
        ])
        for orden in ordenes:
            writer.writerow([
                orden.numero,
                orden.fecha_orden_fabricacion.strftime('%d/%m/%Y') if orden.fecha_orden_fabricacion else '',
                str(orden.id_modelo),
                orden.descripcion,
                orden.info_adicional,
                str(orden.id_cortador),
                str(orden.id_sucursal),
                str(orden.id_estatus),
                str(orden.id_vendedor),
                str(orden.id_armador),
                str(orden.id_empacador),
                str(orden.id_hilos),
                str(orden.id_proposito_id),
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
