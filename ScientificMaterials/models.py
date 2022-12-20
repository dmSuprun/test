import uuid

from django.contrib.auth.models import User
from django.db import models

class ScientificMaterials(models.Model):
    material_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_name = models.CharField('Назва матеріалу', max_length=255)
    key_words = models.CharField('Ключові поняття', max_length=255)
    material = models.TextField('Матеріал')
    author = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Автор матеріалу')

