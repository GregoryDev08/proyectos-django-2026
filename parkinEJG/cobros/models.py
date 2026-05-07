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
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")

    def __str__(self):
        return f"{self.numero_placa} - {self.cliente}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['numero_placa']
