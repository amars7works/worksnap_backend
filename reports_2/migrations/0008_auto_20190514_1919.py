# Generated by Django 2.1 on 2019-05-14 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports_2', '0007_auto_20190514_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyleave',
            name='leave_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default=(('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')), max_length=25),
        ),
    ]
