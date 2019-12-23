# Generated by Django 3.0 on 2019-12-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.CharField(max_length=1000)),
                ('sender_acct', models.CharField(max_length=1000)),
                ('amount', models.CharField(max_length=1000)),
                ('date', models.CharField(max_length=1000)),
                ('receiver_acct', models.CharField(max_length=1000)),
                ('debit_customer', models.CharField(max_length=1000)),
                ('credit_customer', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'history',
            },
        ),
    ]
