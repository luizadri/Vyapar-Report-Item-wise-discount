# Generated by Django 3.2.23 on 2023-12-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vyaparapp', '0016_auto_20231214_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentout',
            name='ref_no',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]