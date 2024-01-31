# Generated by Django 5.0.1 on 2024-01-31 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Costumers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(max_length=16, unique=True)),
                ('discount_type', models.CharField(blank=True, choices=[('P', 'Percent'), ('F', 'Fixed')], max_length=10, null=True)),
                ('discount', models.IntegerField(max_length=100000000)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_subcat', models.BooleanField(default=False)),
                ('pic', models.ImageField(upload_to='static/img')),
                ('parent_category', models.ForeignKey(blank=True, limit_choices_to={'is_subcat': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcat', to='Product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=30)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('manufator_date', models.DateField()),
                ('pic', models.ImageField(upload_to='static/img')),
                ('category', models.ForeignKey(limit_choices_to={'is_subcat': True}, on_delete=django.db.models.deletion.CASCADE, to='Product.category', verbose_name='Selected Subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.TextField(max_length=2000)),
                ('rating', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Costumers.costumer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
            ],
        ),
    ]