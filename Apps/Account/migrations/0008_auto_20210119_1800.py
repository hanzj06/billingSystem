# Generated by Django 3.1.4 on 2021-01-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_auto_20210119_1738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountdetail',
            options={'verbose_name': '账目明细表', 'verbose_name_plural': '账目明细表'},
        ),
        migrations.AlterField(
            model_name='accountdetail',
            name='creditamount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='贷方金额'),
        ),
        migrations.AlterField(
            model_name='accountdetail',
            name='debitamount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='借方金额'),
        ),
    ]
