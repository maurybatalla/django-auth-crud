from django.contrib import admin
from .models import Task

## esto me permite ver el campo created de solo lectura en el modificar del crud que crea el admin
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Task,TaskAdmin)
# esto me sirve para poder manejar la tabla tareas desde el admin
