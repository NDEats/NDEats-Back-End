# Generated by Django 3.2.16 on 2022-12-03 20:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('venmo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropoff', models.CharField(max_length=200)),
                ('pickup', models.CharField(max_length=200)),
                ('tip', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(50.0)])),
                ('available', models.BooleanField(default=True)),
                ('readyBy', models.TimeField()),
                ('delivererId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Deliverer', to='ndeatsApp.person')),
                ('ordererId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orderer', to='ndeatsApp.person')),
            ],
        ),
        migrations.CreateModel(
            name='OldOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dropoff', models.CharField(max_length=200)),
                ('pickup', models.CharField(max_length=200)),
                ('tip', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(50.0)])),
                ('readyBy', models.TimeField()),
                ('delivererId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='OldDeliverer', to='ndeatsApp.person')),
                ('ordererId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OldOrderer', to='ndeatsApp.person')),
            ],
        ),
    ]