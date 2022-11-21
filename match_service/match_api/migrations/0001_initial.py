# Generated by Django 4.1.3 on 2022-11-21 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(max_length=255)),
                ('visitor', models.CharField(max_length=255)),
                ('alignment', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('weather', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('created_by_local', models.BooleanField()),
                ('accepted', models.BooleanField()),
            ],
        ),
    ]
