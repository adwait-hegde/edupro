# Generated by Django 3.2.6 on 2021-08-07 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='rts',
            new_name='teacher',
        ),
    ]
