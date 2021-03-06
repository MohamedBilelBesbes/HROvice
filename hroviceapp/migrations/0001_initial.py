# Generated by Django 3.2.5 on 2021-10-17 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Intern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('cin', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('phonenumber', models.IntegerField()),
                ('school', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dateinit', models.DateField()),
                ('dateend', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('signer', models.CharField(max_length=200)),
                ('dateofsign', models.DateField()),
                ('intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hroviceapp.intern')),
            ],
        ),
    ]
