"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('taks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('marcas/', views.marcas_list, name='marcas_list'),
    path('marcas/nueva/', views.marcas_create, name='marcas_create'),
    path('marcas/editar/<int:pk>/', views.marcas_update, name='marcas_update'),
    path('marcas/eliminar/<int:pk>/', views.marcas_delete, name='marcas_delete'),
    path('hilos/', views.hilos_list, name='hilos_list'),
    path('hilos/nueva/', views.hilos_create, name='hilos_create'),
    path('hilos/editar/<int:pk>/', views.hilos_update, name='hilos_update'),
    path('hilos/eliminar/<int:pk>/', views.hilos_delete, name='hilos_delete'),
    path('personal/', views.personal_list, name='personal_list'),
    path('personal/nueva/', views.personal_create, name='personal_create'),
    path('personal/editar/<int:pk>/', views.personal_update, name='personal_update'),
    path('personal/eliminar/<int:pk>/', views.personal_delete, name='personal_delete'),
    path('modelos/', views.modelos_list, name='modelos_list'),
    path('modelos/nueva/', views.modelos_create, name='modelos_create'),
    path('modelos/editar/<int:pk>/', views.modelos_update, name='modelos_update'),
    path('modelos/eliminar/<int:pk>/', views.modelos_delete, name='modelos_delete'),
    path('modelos/imprimir/<int:pk>/', views.modelos_print, name='modelos_print'),
    path('sucursales/', views.sucursal_list, name='sucursal_list'),
    path('sucursales/nueva/', views.sucursal_create, name='sucursal_create'),
    path('sucursales/editar/<int:pk>/', views.sucursal_update, name='sucursal_update'),
    path('sucursales/eliminar/<int:pk>/', views.sucursal_delete, name='sucursal_delete'),
    path('ordenes/', views.orden_list, name='orden_list'),
    path('ordenes/nueva/', views.orden_create, name='orden_create'),
    path('ordenes/editar/<int:pk>/', views.orden_update, name='orden_update'),
    path('ordenes/eliminar/<int:pk>/', views.orden_delete, name='orden_delete'),
    path('ordenes/imprimir/<int:pk>/', views.orden_print, name='orden_print'),
 ]
