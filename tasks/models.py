from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username


class Marcas(models.Model):
    id_marcas = models.AutoField(primary_key=True, db_column='id_marcas')
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
      db_table = 'iom_marcas'
    def clean(self):
        self.nombre = self.nombre.upper()
        if Marcas.objects.exclude(pk=self.pk).filter(nombre=self.nombre).exists():
            raise ValidationError({'nombre': 'El nombre ya existe.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True, db_column='id_sucursal')
    nombre = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
  
    class Meta:
      db_table = 'iom_sucursales'
 
    def clean(self):
        self.nombre = self.nombre.upper()
        if Sucursal.objects.exclude(pk=self.pk).filter(nombre=self.nombre).exists():
            raise ValidationError({'nombre': 'El nombre ya existe.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
      
class Personal(models.Model):
    id_personal = models.AutoField(primary_key=True, db_column='id_personal')
    nombre = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, unique=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)  # <-- agrega esta línea
    # Agrega los campos booleanos para los roles
    cortador = models.BooleanField(default=False)  # <-- agrega esta línea
    vendedor = models.BooleanField(default=False)  # <-- agrega esta línea
    armador = models.BooleanField(default=False)  # <-- agrega esta línea 
    empacador = models.BooleanField(default=False)  # <-- agrega esta línea
    activo = models.BooleanField(default=True)

    # otros campos...

    class Meta:
      db_table = 'iom_personal'

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class Estatus(models.Model):
    id_estatus = models.AutoField(primary_key=True, db_column='id_estatus')
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
      db_table = 'iom_estatus'
    def clean(self):
        self.nombre = self.nombre.upper()
        if Marcas.objects.exclude(pk=self.pk).filter(nombre=self.nombre).exists():
            raise ValidationError({'nombre': 'El nombre ya existe.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Hilos(models.Model):
    id_hilos = models.AutoField(primary_key=True, db_column='id_hilos')
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    # otros campos...

    class Meta:
      db_table = 'iom_hilos'

    def __str__(self):
        return self.nombre

class Proposito(models.Model):
    id_proposito = models.AutoField(primary_key=True, db_column='id_proposito')
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
      db_table = 'iom_proposito'

    def __str__(self):
        return self.nombre

class Modelos(models.Model):
    id_modelos = models.AutoField(primary_key=True, db_column='id_modelos')
    nombre = models.CharField(max_length=50)
    id_marcas = models.ForeignKey(Marcas, related_name='modelos_marcas', on_delete=models.PROTECT,db_column='id_marcas')
    fecha_ini = models.SmallIntegerField(default=0)
    fecha_ter = models.SmallIntegerField(default=0) 
    activo = models.BooleanField(default=True)
    num_asientos = models.SmallIntegerField(default=0)
    num_filas = models.SmallIntegerField(default=0)
    serie = models.CharField(max_length=20)
    accesorios = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
      db_table = 'iom_modelos'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class OrdenFabricacionEnc(models.Model):
    id_orden_fabricacion = models.AutoField(primary_key=True,db_column='id_orden_fabricacion')
    numero = models.BigIntegerField(unique=True)
    fecha_orden_fabricacion = models.DateField()
    id_modelo = models.ForeignKey(Modelos, on_delete=models.PROTECT,db_column='id_modelos')  
    descripcion = models.CharField(max_length=50)
    info_adicional = models.CharField(max_length=100)
    id_cortador = models.ForeignKey(Personal, related_name='ordenes_cortador', on_delete=models.PROTECT,db_column='id_cortador')
    fecha_corte = models.DateField()
    fecha_armado = models.DateField()
    fecha_embalaje = models.DateField()
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT,db_column='id_sucursal')
    id_estatus = models.ForeignKey(Estatus, on_delete=models.PROTECT,db_column='id_estatus')
    activo = models.BooleanField(default=True)
    id_vendedor = models.ForeignKey(Personal, related_name='ordenes_vendedor', on_delete=models.PROTECT,db_column='id_vendedor')
    id_armador = models.ForeignKey(Personal, related_name='ordenes_armador', on_delete=models.PROTECT,db_column='id_armador')
    id_empacador = models.ForeignKey(Personal, related_name='ordenes_empacador', on_delete=models.PROTECT,db_column='id_empacador')
    id_hilos = models.ForeignKey(Hilos, on_delete=models.PROTECT,db_column='id_hilos')
    id_proposito = models.ForeignKey(Proposito, on_delete=models.PROTECT,db_column='id_proposito')

    class Meta:
        db_table = 'iom_orden_fabricacion_enc'
    
    def __str__(self):
        return f"Orden #{self.numero}"