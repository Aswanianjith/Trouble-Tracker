# Generated by Django 5.0.1 on 2024-06-08 08:43

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trouble_app', '0006_alter_issue_created_by_alter_issue_priority_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Attachment', 'verbose_name_plural': 'Attachments'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-created_at'], 'verbose_name': 'Issue', 'verbose_name_plural': 'Issues'},
        ),
        migrations.AddField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=20),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], default='Open', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together={('title', 'created_by')},
        ),
    ]
