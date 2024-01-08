# Generated by Django 4.0.3 on 2024-01-08 03:43

from django.db import migrations, models
import medicalManagerWeb.core.enums
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('medicalManagerWeb', '0005_alter_doctor_id_alter_keytoken_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[(medicalManagerWeb.core.enums.GENDER['M'], 'Male'), (medicalManagerWeb.core.enums.GENDER['F'], 'Female'), (medicalManagerWeb.core.enums.GENDER['O'], 'Other')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('note', models.TextField(blank=True)),
                ('allergies', models.TextField()),
            ],
        ),
    ]
