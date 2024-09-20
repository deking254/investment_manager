import pytest
import logging
from django.contrib.auth.models import User, Group, Permission
from investmentmanager.models import Transaction
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
#creates an admin django account

@pytest.fixture
def admin_user(db):
    # Create an admin user
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )
    return user

@pytest.fixture
def create_groups(admin_user, db):
    # Create three groups and assign permissions
    groups = []
    permissions =[]
    #find the permissions
    content_type = ContentType.objects.get_for_model(Transaction)
    permissions = Permission.objects.filter(content_type=content_type)
    # Create the groups
    group1, created = Group.objects.get_or_create(name='investmentacc1')
    group1.permissions.add(permissions.get(codename='view_transaction'))
    groups.append(group1)
    group2, created = Group.objects.get_or_create(name='investmentacc2')
    for permission in permissions:
        group2.permissions.add(permission)
    groups.append(group2)
    group3, created = Group.objects.get_or_create(name='investmentacc3')
    group3.permissions.add(permissions.get(codename='add_transaction'))
    groups.append(group3)
    
    return groups

# create an investment accounts with permissions
@pytest.fixture
def investmentacc1() -> Group:
    return Group.objects.create(name='investment account 1')
# create a user object in investment accounts

@pytest.fixture
def investmentacc1usr(create_groups, db) -> User:
    usracc1 = User.objects.create_user(username="investmentacc1usr", email='dennis@actserv.com', first_name='Dennis', last_name='kiptoo', password="testpassword")
    usracc1.groups.add(create_groups[0])
    return usracc1

@pytest.fixture
def investmentacc2usr(create_groups, db) -> User:
    usracc2 = User.objects.create_user(username="investmentacc2usr", email='joy@actserv.com', first_name='Joy', last_name='mwihaki', password="testpassword")
    usracc2.groups.add(create_groups[0])
    return usracc2

@pytest.fixture
def investmentacc3usr(create_groups, db) -> User:
    usracc3 = User.objects.create_user(username="investmentacc3usr", email='hillary@actserv.com', first_name='Hillary', last_name='Juma', password="testpassword")
    usracc3.groups.add(create_groups[2])
    return usracc3

@pytest.fixture
def investmentacc1usrpost(investmentacc1usr) -> dict:
    return {

        "username": "dekingsky",
        "first_name": "Dennis",
        "last_name": "Ngetich",
        "password": "testpass254",
        "groups": [investmentacc1usr.groups]
    }
@pytest.fixture
def transaction_investmentacc1usr(investmentacc1usr) -> dict:
    return {
        "transactiontype": "deposit",
        "amount": "500",
        "description": "To buy some bonds",
        "user": [investmentacc1usr]

    }

@pytest.fixture()
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()
