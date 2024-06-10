# Generated by Django 4.2.5 on 2024-06-07 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_agriculturalorganization_licence_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agriculturalorganization',
            name='email',
        ),
        migrations.AddField(
            model_name='agriculturalorganization',
            name='Licence',
            field=models.FileField(blank=True, null=True, upload_to='static/uploads/licences'),
        ),
        migrations.AddField(
            model_name='agriculturalorganization',
            name='communicationOfficer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='communication_officer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agriculturalorganization',
            name='contact',
            field=models.CharField(default='+256771183868', max_length=15),
        ),
    ]
