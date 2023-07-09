from django.db import models
from django.contrib.auth.models import User
# Create your models here.

##python manage.py makemigrations      - para crear una migracion con los cambios
## python manage.py migrations          - para ejecutar esa migracion y asnetar los cambios en la base de datos 
## python manage.py createsuperuser para crear usuario en el admin de django
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    ## on_delete=models.CASCADE esto lo que hace es que si borramos el usuario borra todo en cascada qeu tenga que ver con ese usuario de las otras tablas 
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + "  - " + self.user.username