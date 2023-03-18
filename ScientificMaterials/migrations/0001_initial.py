# Generated by Django 4.1.6 on 2023-03-04 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScientificMaterials',
            fields=[
                ('material_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('material_name', models.CharField(max_length=255, verbose_name='Назва матеріалу')),
                ('key_words', models.CharField(max_length=255, verbose_name='Ключові поняття')),
                ('material', models.TextField(verbose_name='Матеріал')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор матеріалу')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]