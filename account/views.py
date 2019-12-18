from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Customer, Account
from django.contrib import messages
from zeep import Client
import string
import random
import uuid


def signup(request):
    client = Client(wsdl='http://3.122.134.94:9095/ibank-test/services?wsdl')
    N = 5
    code = ''.join(random.choices(string.digits, k=N))
    cus_id = str(code)
    mnemo = uuid.uuid4().hex[:5].upper()
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        username = request.POST['username']
        title = request.POST['title']
        gender = request.POST['gender']
        email = request.POST['email']
        initial = request.POST['initial']
        mobile = request.POST['mobile']
        address = request.POST['address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mode_of_id = request.POST['mode_of_id']
        id_no = request.POST['id_no']
        nationality = request.POST['nationality']
        residence = request.POST['residence']
        dob = request.POST['dob']
        m_status = request.POST['m_status']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email Taken')
                return redirect('signup')
            else:
                req_data = {
                    'WebRequestCommon': {
                        'company': 'NG0010001',
                        'password': 'QWERTY',
                        'userName': 'JMIG02',
                    },
                    'OfsFunction': {
                        'activityName': '',
                        'assignReason': '',
                        'dueDate': '',
                        'extProcess': '',
                        'extProcessID': '',
                        'gtsControl': '',
                        'messageId': '',
                        'noOfAuth': '',
                        'owner': '',
                        'replace': '',
                        'startDate': '',
                        'user': ''
                    },
                    'CUSTOMERIBINDIVType': {
                        'Mnemonic': initial + mnemo,
                        'gSHORTNAME': {
                            'Surname': surname
                        },
                        'gNAME1': {
                            'FirstNames': first_name
                        },
                        'gNAME2': {
                            'PreferredName': last_name
                        },
                        'gSTREET': {
                            'PhysicalAddress': address
                        },
                        'Sector': '7001',
                        'AccountOfficer': '8000',
                        'Industry': '7000',
                        'Nationality': nationality,
                        'Residence': residence,
                        'gLEGALID': {
                            'IDPassportNo': id_no
                        },
                        'DateofBirth': dob,
                        'Title': title,
                        'Gender': gender,
                        'MaritalStatus': m_status,
                        'Initials': initial,
                        'MobilePhoneNo': mobile,
                        'ResidentYN': 'Y',
                        'CustomerOpeningDate': '',
                        'IDType': mode_of_id,
                        'EducationLevel': '3',
                        'CustomersLanguage': '1',
                        'IBCustomerID': 'IB' + cus_id

                    }
                }
                response = client.service.CreateIBCustomer(**req_data)
                # print(response)
                if response.Status.successIndicator == 'Success':
                    c_no = response.CUSTOMERType.id
                    mnemonic = response.CUSTOMERType.MNEMONIC
                    short_name = response.CUSTOMERType.gSHORTNAME.SHORTNAME
                    name1 = response.CUSTOMERType.gNAME1.NAME1
                    name2 = response.CUSTOMERType.gNAME2.NAME2
                    tit = response.CUSTOMERType.TITLE
                    id_num = response.CUSTOMERType.gLEGALIDDOCNAME.LEGALIDDOCNAME
                    d_o_b = response.CUSTOMERType.BIRTHINCORPDATE
                    gend = response.CUSTOMERType.GENDER
                    marital = response.CUSTOMERType.MARITALSTATUS
                    mobile_no = response.CUSTOMERType.TELMOBILE
                    o_date = response.CUSTOMERType.OPENINGDATE
                    ib_cus_id = response.CUSTOMERType.IBCUSTOMERID

                    user = User.objects.create_user(username=username,
                                                    password=password1,
                                                    email=email,
                                                    first_name=surname,
                                                    last_name=first_name)
                    cus = Customer(customer_no=c_no,
                                   mnemonic=mnemonic,
                                   short_name=short_name,
                                   name1=name1,
                                   name2=name2,
                                   title=tit,
                                   street=address,
                                   id_no=id_num,
                                   dob=d_o_b,
                                   gender=gend,
                                   marital_status=marital,
                                   mobile_no=mobile_no,
                                   o_date=o_date,
                                   ib_customer_id=ib_cus_id,
                                   cus_user=username)
                    user.save()
                    cus.save()
                    messages.success(request, 'Registration Successful')
                    return redirect('signup')
                else:
                    messages.error(request, 'Registration Fail, Please Try Again')
                    return redirect('signup')

    return render(request, 'signup.html')


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        ib_id = request.POST['ib_id']

        user = auth.authenticate(username=username, password=password)
        if Customer.objects.filter(ib_customer_id=ib_id).exists() and user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login Details')
            return redirect('index')
    else:
        return render(request, 'index.html')


@login_required(login_url='/account/index')
def home(request):
    return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def profile(request):
    c_user = request.user.username
    show = Customer.objects.all().get(cus_user=c_user)
    context = {'show': show}
    return render(request, 'profile.html', context)


@login_required(login_url='/account/index')
def create_acct(request):
    client = Client(wsdl='http://3.122.134.94:9095/ibank-test/services?wsdl')
    c_user = request.user.username
    if request.method == 'POST':
        currency = request.POST['currency']
        acct_type = request.POST['acct_type']
        cus_no = Customer.objects.values('customer_no').get(cus_user=c_user)['customer_no']
        ib_cus_code = Customer.objects.values('ib_customer_id').get(cus_user=c_user)['ib_customer_id']
        print('HELLO: ' + ib_cus_code)
        if Account.objects.filter(acct_user=c_user, acct_category=acct_type).exists():
            messages.error(request, "Please you already have this category of Account")
            return redirect('create_acct')
        else:
            req_data = {
                'WebRequestCommon': {
                    'company': 'NG0010001',
                    'password': 'QWERTY',
                    'userName': 'JMIG02',
                },
                'OfsFunction': {
                    'activityName': '',
                    'assignReason': '',
                    'dueDate': '',
                    'extProcess': '',
                    'extProcessID': '',
                    'gtsControl': '',
                    'messageId': '',
                    'noOfAuth': '',
                    'owner': '',
                    'replace': '',
                    'startDate': '',
                    'user': ''
                },
                'ACCOUNTIBCREATEType': {
                    'CustomerNumber': cus_no,
                    'Category': acct_type,
                    'AccountName': '',
                    'AccountMnemonic': '',
                    'Currency': currency,
                    'AccountOfficer': '8000',
                    'IBCustomerID': ib_cus_code
                }
            }
            response = client.service.CreateIBAccount(**req_data)
            print(response)
            if response.Status.successIndicator == 'Success':
                cust_no = response.ACCOUNTType.CUSTOMER
                acct_mnemonic = response.ACCOUNTType.MNEMONIC
                acct_cat = response.ACCOUNTType.CATEGORY
                acct_officer = response.ACCOUNTType.ACCOUNTOFFICER
                acct_currency = response.ACCOUNTType.CURRENCY
                acct_open_date = response.ACCOUNTType.OPENINGDATE
                acct_no = response.ACCOUNTType.id
                ib_cus_id = response.ACCOUNTType.IBCUSTOMERID

                acct = Account(acct_user=c_user,
                               customer_no=cust_no,
                               acct_mnemonic=acct_mnemonic,
                               acct_category=acct_cat,
                               acct_officer=acct_officer,
                               acct_currency=acct_currency,
                               acct_open_date=acct_open_date,
                               acct_no=acct_no,
                               cus_id=ib_cus_id)
                acct.save()
                messages.success(request, 'Account Created')
                return redirect('create_acct')
            else:
                messages.error(request, 'Fail, Please Try Again')
                return redirect('create_acct')
    return render(request, 'create_acct.html')


@login_required(login_url='/account/index')
def acct_list(request):
    c_user = request.user.username
    show = Account.objects.filter(acct_user=c_user)
    context = {'show': show}
    return render(request, 'acct_list.html', context)


@login_required(login_url='/account/index')
def fund_transfer(request):
    client = Client(wsdl='http://3.122.134.94:9095/ibank-test/services?wsdl')
    c_user = request.user.username
    show = Account.objects.filter(acct_user=c_user)
    context = {'show': show}
    if request.method == 'POST':
        s_acct = request.POST['s_acct']
        r_acct = request.POST['r_acct']
        amount = request.POST['amount']
        comment = request.POST['comment']
        req_data = {
            'WebRequestCommon': {
                'company': 'NG0010001',
                'password': 'QWERTY',
                'userName': 'IBUSER.1',
            },
            'OfsFunction': {
                'activityName': '',
                'assignReason': '',
                'dueDate': '',
                'extProcess': '',
                'extProcessID': '',
                'gtsControl': '',
                'messageId': '',
                'noOfAuth': '',
                'owner': '',
                'replace': '',
                'startDate': '',
                'user': ''
            },
            'FUNDSTRANSFERIBType': {
                'DebitAccount': s_acct,
                'DebitCurrency': 'NGN',
                'DebitAmount': amount,
                'DebitValueDate': '',
                'CreditAccount': r_acct,
                'CreditCurrency': 'NGN',
                'CreditValueDate': '',
                'TreasuryRate': '',
                'gORDERINGCUST': {
                    'OrderedBy': comment
                }
            }
        }
        response = client.service.IBFT(**req_data)
        print(response)
        if response.Status.successIndicator == 'Success':
            messages.success(request, 'Transaction Successful')
            return redirect('fund_transfer')
        else:
            messages.error(request, 'Fail')
            return redirect('fund_transfer')
    return render(request, 'fund_transfer.html', context)
