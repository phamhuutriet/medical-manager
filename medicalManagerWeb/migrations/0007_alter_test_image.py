# Generated by Django 4.0.3 on 2024-03-28 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalManagerWeb', '0006_alter_test_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]