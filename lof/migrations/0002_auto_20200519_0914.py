# Generated by Django 3.0.3 on 2020-05-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lof', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]