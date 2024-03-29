# Generated by Django 2.2.3 on 2019-07-18 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Swiped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('sid', models.IntegerField()),
                ('mark', models.CharField(choices=[('like', '喜欢'), ('dislike', '不喜欢'), ('superlike', '超级喜欢')], max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'swiped',
            },
        ),
    ]
