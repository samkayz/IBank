# Generated by Django 3.0 on 2019-12-17 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20191216_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acct_user', models.CharField(max_length=1000)),
                ('customer_no', models.CharField(max_length=100)),
                ('acct_mnemonic', models.CharField(max_length=1000)),
                ('acct_category', models.CharField(max_length=100)),
                ('acct_officer', models.CharField(max_length=100)),
                ('acct_currency', models.CharField(max_length=100)),
                ('acct_open_date', models.CharField(max_length=100)),
                ('acct_no', models.CharField(max_length=100)),
                ('cus_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
