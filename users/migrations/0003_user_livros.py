# Generated by Django 5.2.3 on 2025-06-23 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='livros',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
