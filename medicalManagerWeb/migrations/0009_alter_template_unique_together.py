# Generated by Django 4.0.3 on 2024-01-10 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicalManagerWeb', '0008_alter_doctor_name_alter_doctor_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='template',
            unique_together={('user', 'name')},
        ),
    ]
