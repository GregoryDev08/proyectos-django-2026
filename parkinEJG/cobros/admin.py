from django.contrib import admin
from django.utils import timezone
from .models import Cliente, Vehiculo, Espacio, Cobro
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone

@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hora_ingreso', 'hora_salida', 'precio_total', 'botones_accion')
    exclude = (
        'cliente_nombre', 'cliente_apellido', 'cliente_email', 'cliente_telefono', 'cliente_dni',
        'vehiculo_numero_placa', 'vehiculo_color', 'vehiculo_modelo'
    )    

    exclude = (
        'cliente_nombre', 'cliente_apellido', 'cliente_email', 'cliente_telefono', 'cliente_dni',
        'vehiculo_numero_placa', 'vehiculo_color', 'vehiculo_modelo'
    )

    readonly_fields = ('hora_ingreso', 'hora_salida', 'tiempo_horas', 'precio_total')
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:cobro_id>/marcar-ingreso/', self.admin_site.admin_view(self.accion_ingreso), name='cobro-ingreso'),
            path('<int:cobro_id>/marcar-salida/', self.admin_site.admin_view(self.accion_salida), name='cobro-salida'),
        ]
        return custom_urls + urls

    def accion_ingreso(self, request, cobro_id):
        cobro = Cobro.objects.get(pk=cobro_id)
        if not cobro.hora_ingreso:
            cobro.hora_ingreso = timezone.now()
            cobro.save()
            self.message_user(request, f"¡Ingreso registrado exitosamente para la placa {cobro.vehiculo_numero_placa}!")
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def accion_salida(self, request, cobro_id):
        cobro = Cobro.objects.get(pk=cobro_id)
        if cobro.hora_ingreso and not cobro.hora_salida:
            cobro.hora_salida = timezone.now()
            cobro.save() 
            self.message_user(request, f"¡Salida registrada! El total a cobrar es: ${cobro.precio_total}")
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def botones_accion(self, obj):
        if not obj.hora_ingreso:
            url = f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/marcar-ingreso/"
            return format_html(
                '<a class="button" style="background-color: #417690; color: white; font-weight: bold;" href="{}">Registrar Ingreso</a>', url
            )
        elif not obj.hora_salida:
            url = f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/marcar-salida/"
            return format_html(
                '<a class="button" style="background-color: #ba2121; color: white; font-weight: bold;" href="{}">Registrar Salida</a>', url
            )
        else:
            return format_html('<b style="color: #28a745;">Pagado</b>')

    botones_accion.short_description = 'Acción Rápida'

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Espacio)
