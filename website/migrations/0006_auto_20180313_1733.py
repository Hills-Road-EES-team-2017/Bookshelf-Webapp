# Generated by Django 2.0.1 on 2018-03-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20180228_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='book',
            name='book_state',
            field=models.IntegerField(choices=[(0, 'available'), (1, 'taking'), (2, 'taken'), (3, 'returning'), (4, 'reserved'), (5, 'taking basket'), (6, 'returning basket')], default=0),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
