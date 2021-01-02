# Generated by Django 3.1.4 on 2021-01-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liverecrecord',
            name='id',
        ),
        migrations.AlterField(
            model_name='liverecrecord',
            name='rec_uuid',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='UUID of record'),
        ),
    ]