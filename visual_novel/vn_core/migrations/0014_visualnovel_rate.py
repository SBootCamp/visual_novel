# Generated by Django 2.0.2 on 2018-03-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vn_core', '0013_add_test_vns_for_chart_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualnovel',
            name='rate',
            field=models.IntegerField(default=0, verbose_name='оценка на VNDb'),
        ),
    ]
