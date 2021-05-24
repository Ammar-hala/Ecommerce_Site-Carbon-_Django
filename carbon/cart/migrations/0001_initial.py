# Generated by Django 3.1 on 2020-12-12 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0002_auto_20201210_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('variations', models.ManyToManyField(blank=True, to='shop.Variation')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
    ]
