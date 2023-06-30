# Generated by Django 4.1.4 on 2023-05-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClickTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_paydoc_id', models.CharField(blank=True, max_length=255, verbose_name='Номер платежа в системе CLICK')),
                ('amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9, verbose_name='Сумма оплаты (в сумах)')),
                ('action', models.CharField(blank=True, max_length=255, null=True, verbose_name='Выполняемое действие')),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('processing', 'processing'), ('confirmed', 'confirmed'), ('canceled', 'canceled'), ('error', 'error')], default='waiting', max_length=25, verbose_name='Статус')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('message', models.TextField(blank=True, default='')),
            ],
        ),
    ]
