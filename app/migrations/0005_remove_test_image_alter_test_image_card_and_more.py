# Generated by Django 5.1.5 on 2025-01-28 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_test_image_card_alter_user_verification_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='image',
        ),
        migrations.AlterField(
            model_name='test',
            name='image_card',
            field=models.ImageField(blank=True, null=True, upload_to='test/'),
        ),
        migrations.AlterField(
            model_name='test',
            name='test_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
