# Generated by Django 3.1.4 on 2021-01-15 03:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsubcode', models.IntegerField(unique=True, verbose_name='明细科目编码')),
                ('dsubname', models.CharField(max_length=64, unique=True, verbose_name='明细科目名称')),
            ],
            options={
                'verbose_name': '明细科目',
                'verbose_name_plural': '明细科目',
            },
        ),
        migrations.CreateModel(
            name='FirstSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fsubcode', models.IntegerField(unique=True, verbose_name='一级科目编码')),
                ('fsubname', models.CharField(max_length=32, unique=True, verbose_name='一级科目名称')),
            ],
            options={
                'verbose_name': '一级科目',
                'verbose_name_plural': '一级科目',
            },
        ),
        migrations.CreateModel(
            name='SecondSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssubcode', models.IntegerField(unique=True, verbose_name='二级科目编码')),
                ('ssubname', models.CharField(max_length=32, unique=True, verbose_name='二级科目名称')),
                ('fathercode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Account.firstsubjects', to_field='fsubcode', verbose_name='所属一级科目')),
            ],
            options={
                'verbose_name': '二级科目',
                'verbose_name_plural': '二级科目',
            },
        ),
        migrations.CreateModel(
            name='AccountingVouchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recordtime', models.DateField(verbose_name='账目发生日期')),
                ('billtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='记账时间')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('voucherno', models.CharField(max_length=15, unique=True, verbose_name='记账凭证编号')),
                ('abstract', models.CharField(blank=True, max_length=300, null=True, verbose_name='账目摘要')),
                ('debitamount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='借方金额')),
                ('creditamount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='贷方金额')),
                ('operatername', models.CharField(max_length=10, verbose_name='录入者')),
                ('voucherfile', models.FileField(blank=True, null=True, upload_to='F:\\Auto Test\\BillingSystem\\upload\\2021-01-15', verbose_name='附件')),
                ('creditdsubcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cdsubcode', to='Account.detailsubjects', to_field='dsubcode', verbose_name='明细科目(贷)')),
                ('creditfsubcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cfsubcode', to='Account.firstsubjects', to_field='fsubcode', verbose_name='一级科目(贷)')),
                ('creditssubcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cssubcode', to='Account.secondsubjects', to_field='ssubcode', verbose_name='二级科目(贷)')),
                ('debitdsubcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ddsubcode', to='Account.detailsubjects', to_field='dsubcode', verbose_name='明细科目(借)')),
                ('debitfsubcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='dfsubcode', to='Account.firstsubjects', to_field='fsubcode', verbose_name='一级科目(借)')),
                ('debitssubcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dssubcode', to='Account.secondsubjects', to_field='ssubcode', verbose_name='二级科目(借)')),
            ],
            options={
                'verbose_name': '账目',
                'verbose_name_plural': '账目登记',
            },
        ),
    ]
