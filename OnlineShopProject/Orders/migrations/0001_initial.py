# Generated by Django 5.0.1 on 2024-02-07 14:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Costumers', '0002_initial'),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_price', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True)),
                ('status', models.CharField(choices=[('R', 'Refunded'), ('C', 'Cancelled'), ('D', 'Delivered'), ('I', 'IN progress')], default='I', max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Costumers.costumer')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.discountcodes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Orders.order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='Orders.orderitem'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency', models.CharField(max_length=3)),
                ('payment_method', models.CharField(choices=[('CA', 'Cash'), ('CR', 'Credit'), ('DC', 'Debit Card')])),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('refund_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('refund_reason', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Costumers.costumer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Orders.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
