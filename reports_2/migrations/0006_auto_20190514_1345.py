# Generated by Django 2.1 on 2019-05-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports_2', '0005_auto_20190514_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyleave',
            name='leave_status',
            field=models.BooleanField(null=True),
        ),
    ]
