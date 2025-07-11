# Generated by Django 5.1.3 on 2024-11-17 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='login_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='expert_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('image', models.FileField(upload_to='')),
                ('phoneno', models.BigIntegerField()),
                ('email', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=50)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login_table')),
            ],
        ),
        migrations.CreateModel(
            name='chat_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=600)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('FROM_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kk', to='myapp.login_table')),
                ('TO_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hh', to='myapp.login_table')),
            ],
        ),
        migrations.CreateModel(
            name='studymaterials_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
                ('details', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('EXPERT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.expert_table')),
            ],
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('image', models.FileField(upload_to='')),
                ('place', models.CharField(max_length=100)),
                ('post', models.CharField(max_length=100)),
                ('pin', models.BigIntegerField()),
                ('phoneno', models.BigIntegerField()),
                ('email', models.CharField(max_length=100)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login_table')),
            ],
        ),
        migrations.CreateModel(
            name='score_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('score', models.FloatField()),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user_table')),
            ],
        ),
        migrations.CreateModel(
            name='feedback_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('date', models.DateField()),
                ('EXPERT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.expert_table')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user_table')),
            ],
        ),
        migrations.CreateModel(
            name='complaint_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.CharField(max_length=600)),
                ('date', models.DateField()),
                ('reply', models.CharField(max_length=600)),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user_table')),
            ],
        ),
        migrations.CreateModel(
            name='work_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('work', models.CharField(max_length=50)),
                ('details', models.CharField(max_length=200)),
                ('response', models.CharField(max_length=600)),
                ('EXPERT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.expert_table')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user_table')),
            ],
        ),
    ]
