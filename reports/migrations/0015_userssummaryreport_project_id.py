# Generated by Django 2.1 on 2019-06-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_auto_20190523_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='userssummaryreport',
            name='project_id',
            field=models.CharField(default=0, max_length=25),
            preserve_default=False,
        ),
    ]
