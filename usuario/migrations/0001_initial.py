# Generated by Django 3.1 on 2020-08-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('username', models.CharField(max_length=256, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=256)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
    ]
