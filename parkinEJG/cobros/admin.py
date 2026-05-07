from django.contrib import admin
from .models import Cliente, Vehiculo, Espacio, Cobro


class CobroAdmin(admin.ModelAdmin):
    readonly_fields = [
        'cliente_nombre',
        'cliente_apellido',
        'cliente_email',
        'cliente_telefono',
        'cliente_dni',
        'vehiculo_numero_placa',
        'vehiculo_color',
        'vehiculo_modelo',
        'precio_total',
    ]
    list_display = ['id', 'cliente', 'vehiculo', 'espacio', 'fecha', 'tiempo_horas', 'precio_total']
    list_filter = ['fecha', 'espacio']
    search_fields = ['cliente_nombre', 'vehiculo_numero_placa', 'cliente_dni']


# Register your models here.
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Espacio)
admin.site.register(Cobro, CobroAdmin)