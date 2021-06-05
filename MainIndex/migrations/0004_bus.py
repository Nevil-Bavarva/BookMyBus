# Generated by Django 3.0.1 on 2021-05-29 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainIndex', '0003_delete_bus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BusName', models.CharField(max_length=250)),
                ('BusNumber', models.CharField(max_length=250)),
                ('BusImage', models.CharField(default='https://i.ytimg.com/vi/FnKM_1TbWJU/hqdefault.jpg', max_length=5000)),
                ('BusCompany', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='MainIndex.Agency')),
            ],
        ),
    ]
