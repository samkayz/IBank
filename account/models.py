from django.db import models


class Customer(models.Model):
    cus_user = models.CharField(max_length=100)
    customer_no = models.CharField(max_length=100)
    mnemonic = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    id_no = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    o_date = models.CharField(max_length=100)
    ib_customer_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'customer'


class Account(models.Model):
    acct_user = models.CharField(max_length=1000)
    customer_no = models.CharField(max_length=100)
    acct_mnemonic = models.CharField(max_length=1000)
    acct_category = models.CharField(max_length=100)
    acct_officer = models.CharField(max_length=100)
    acct_currency = models.CharField(max_length=100)
    acct_open_date = models.CharField(max_length=100)
    acct_no = models.CharField(max_length=100)
    cus_id = models.CharField(max_length=100)
    balance = models.CharField(max_length=1000)

    class Meta:
        db_table = 'account'


class History(models.Model):
    trans_id = models.CharField(max_length=1000)
    sender_acct = models.CharField(max_length=1000)
    amount = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    receiver_acct = models.CharField(max_length=1000)
    debit_customer = models.CharField(max_length=1000)
    credit_customer = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)

    class Meta:
        db_table = 'history'

