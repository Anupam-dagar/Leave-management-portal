# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-23 20:55
from __future__ import unicode_literals

import cloudinary.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('department', models.CharField(choices=[('MP&GS', 'MP&GS'), ('O&M1', 'O&M1'), ('O&M2', 'QAO&M2'), ('M&T', 'M&T'), ('MM&Store', 'MM&Store'), ('Civil', 'Civil'), ('CE', 'CE')], default='', max_length=200)),
                ('available_leaves', models.IntegerField(default=15)),
                ('designation', models.CharField(choices=[('CE', 'CE'), ('SE', 'SE'), ('XEN', 'XEN'), ('AEE', 'AEE')], max_length=200)),
                ('power_station', models.CharField(choices=[('Hisar', 'Hisar'), ('Panipat', 'Panipat'), ('Yamuna Nagar', 'Yamuna Nagar'), ('Panchkula', 'Panchkula')], default='', max_length=200)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('purpose', models.CharField(max_length=1200)),
                ('approval', models.BooleanField(default=False)),
                ('leave_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('noted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_notedby', to=settings.AUTH_USER_MODEL)),
                ('noted_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_notedto', to=settings.AUTH_USER_MODEL)),
                ('sanctioned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_sanctioned', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
