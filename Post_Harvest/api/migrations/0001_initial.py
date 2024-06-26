# Generated by Django 4.2.5 on 2024-05-31 09:36

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('OTP', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.FileField(blank=True, null=True, upload_to='static/uploads/photos')),
                ('role', models.CharField(choices=[('farmer', 'Farmer'), ('comm_officer', 'Communication Officer'), ('admin', 'Admin')], default='farmer', max_length=20)),
                ('isApproved', models.BooleanField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('variety', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('instructions', models.TextField()),
                ('tutorial', models.FileField(upload_to='')),
                ('type', models.CharField(max_length=10)),
                ('frequency', models.CharField(blank=True, max_length=50, null=True)),
                ('controltiming', models.CharField(blank=True, max_length=50, null=True)),
                ('communicationOfficer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_communication_officer', to=settings.AUTH_USER_MODEL)),
                ('farmer', models.ManyToManyField(related_name='farmer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostHarvestTechnique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop', to='api.crop')),
            ],
        ),
        migrations.CreateModel(
            name='Pest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('preferredHabitat', models.TextField()),
                ('commonDamage', models.TextField()),
                ('lifecycle', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('pestControl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pest_control', to='api.information')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('instruction', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('technique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_harvest_technique', to='api.postharvesttechnique')),
            ],
        ),
        migrations.AddField(
            model_name='crop',
            name='pests',
            field=models.ManyToManyField(related_name='pest', to='api.pest'),
        ),
        migrations.CreateModel(
            name='AgriculturalOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=15)),
                ('Licence', models.FileField(upload_to='')),
                ('communicationOfficer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='communication_officer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
