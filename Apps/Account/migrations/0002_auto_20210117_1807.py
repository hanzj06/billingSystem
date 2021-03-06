# Generated by Django 3.1.4 on 2021-01-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csubcode', models.IntegerField(unique=True, verbose_name='现金段编码')),
                ('csubname', models.CharField(max_length=64, unique=True, verbose_name='现金段名称')),
            ],
            options={
                'verbose_name': '现金段',
                'verbose_name_plural': '现金段',
            },
        ),
        migrations.AlterModelOptions(
            name='detailsubjects',
            options={'verbose_name': '明细段', 'verbose_name_plural': '明细段'},
        ),
        migrations.AlterField(
            model_name='accountingvouchers',
            name='voucherfile',
            field=models.FileField(blank=True, null=True, upload_to='F:\\Auto Test\\BillingSystem\\upload\\2021-01-17', verbose_name='附件'),
        ),
        migrations.AlterField(
            model_name='detailsubjects',
            name='dsubcode',
            field=models.IntegerField(unique=True, verbose_name='明细段编码'),
        ),
        migrations.AlterField(
            model_name='detailsubjects',
            name='dsubname',
            field=models.CharField(max_length=64, unique=True, verbose_name='明细段名称'),
        ),
    ]
