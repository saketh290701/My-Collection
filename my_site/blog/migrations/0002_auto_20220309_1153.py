# Generated by Django 3.2.9 on 2022-03-09 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_name',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='posts'),
        ),
        migrations.AlterField(
            model_name='post',
            name='completed_date',
            field=models.DateField(),
        ),
    ]
