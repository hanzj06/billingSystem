# Generated by Django 3.1.4 on 2021-01-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_auto_20210118_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='subtype',
            field=models.SmallIntegerField(max_length=2, verbose_name='科目类别'),
        ),
    ]
