# Generated by Django 2.0.2 on 2018-07-14 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinfo', '0003_add_translators_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='translator',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='базовая ссылка'),
        ),
    ]