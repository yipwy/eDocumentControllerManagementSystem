# Generated by Django 2.2.3 on 2019-07-19 01:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='SeriesNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_code', models.CharField(max_length=20)),
                ('series_description', models.CharField(max_length=50)),
                ('starting_number', models.IntegerField()),
                ('ending_number', models.IntegerField()),
                ('next_number', models.IntegerField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modify_by', models.CharField(max_length=20)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'SeriesNumbers',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_id', models.CharField(max_length=15)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generals.Branch')),
            ],
            options={
                'verbose_name_plural': 'Warehouses',
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_code', models.CharField(max_length=20)),
                ('document_description', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modify_by', models.CharField(max_length=20)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('document_number_seriesId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='generals.SeriesNumber')),
            ],
            options={
                'verbose_name_plural': 'DocumentTypes',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=20)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generals.Branch')),
            ],
            options={
                'verbose_name_plural': 'Departments',
            },
        ),
    ]