from decimal import Decimal
from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']


class Vehiculo(models.Model):
    numero_placa = models.CharField(max_length=10, unique=True, verbose_name="Número de Placa")
    color = models.CharField(max_length=50, verbose_name="Color")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")

    def __str__(self):
        return f"{self.numero_placa} - {self.cliente}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['numero_placa']


class Espacio(models.Model):
    TIPO_CHOICES = [
        ('vehiculo', 'Vehiculo'),
        ('moto', 'Moto'),
        ('discapacitado', 'Discapacitado'),
    ]

    numero_espacio = models.CharField(max_length=10, unique=True, verbose_name="Número de Espacio")
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vehículo Asignado")
    tipo_espacio = models.CharField(max_length=20, choices=TIPO_CHOICES, default='normal', verbose_name="Tipo de Espacio")

    def __str__(self):
        return f"Espacio {self.numero_espacio}"

    class Meta:
        verbose_name = "Espacio"
        verbose_name_plural = "Espacios"
        ordering = ['numero_espacio']


class Cobro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name="Vehículo")
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, verbose_name="Espacio")
    # fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    hora_ingreso = models.DateTimeField(null=True, verbose_name="Hora de Ingreso")
    hora_salida = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Salida")

    tiempo_horas = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), editable=False, verbose_name="Tiempo en Horas")
    costo_por_hora = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.75'), verbose_name="Costo por Hora")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False, verbose_name="Precio Total")

    cliente_nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre Cliente")
    cliente_apellido = models.CharField(max_length=100, blank=True, null=True, verbose_name="Apellido Cliente")
    cliente_email = models.EmailField(blank=True, null=True, verbose_name="Email Cliente")
    cliente_telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono Cliente")
    cliente_dni = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI Cliente")

    vehiculo_numero_placa = models.CharField(max_length=10, blank=True, null=True, verbose_name="Placa Vehículo")
    vehiculo_color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color Vehículo")
    vehiculo_modelo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modelo Vehículo")

    def save(self, *args, **kwargs):
        self.cliente_nombre = self.cliente.nombre
        self.cliente_apellido = self.cliente.apellido
        self.cliente_email = self.cliente.email
        self.cliente_telefono = self.cliente.telefono
        self.cliente_dni = self.cliente.dni

        self.vehiculo_numero_placa = self.vehiculo.numero_placa
        self.vehiculo_color = self.vehiculo.color
        self.vehiculo_modelo = self.vehiculo.modelo

        if self.hora_salida and self.hora_ingreso:
            diferencia = self.hora_salida - self.hora_ingreso
            
            horas_exactas = Decimal(diferencia.total_seconds()) / Decimal('3600')
            
            self.tiempo_horas = round(horas_exactas, 2)
            precio_calculado = self.tiempo_horas * self.costo_por_hora

            if precio_calculado < self.costo_por_hora:
                self.precio_total = self.costo_por_hora
            else:
                self.precio_total = precio_calculado
                
        else:
            self.tiempo_horas = Decimal('0.00')
            self.precio_total = Decimal('0.00')
        
        if self.hora_salida:
            if self.espacio.vehiculo == self.vehiculo:
                self.espacio.vehiculo = None
                self.espacio.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cobro #{self.pk} - {self.vehiculo_numero_placa}"

    class Meta:
        verbose_name = "Cobro"
        verbose_name_plural = "Cobros"
        ordering = ['-hora_ingreso']
