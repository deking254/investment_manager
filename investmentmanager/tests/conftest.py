import pytest
from django.contrib.auth import User
from rest_framework.test import APIClient
# create a user object in investment account 1
@pytest.fixture
def investmentacc1usr() -> User:
    return User.objects.create_user(username="investmentacc1usr", email='dennis@actserv.com', firstname='Dennis', lastname='kiptoo', password="testpassword")

@pytest.fixture
def investmentacc2usr() -> User:
    return User.objects.create_user(username="investmentacc2usr", email='joy@actserv.com', firstname='Joy', lastname='mwihaki', password="testpassword")

@pytest.fixture
def investmentacc3usr() -> User:
    return User.objects.create_user(username="investmentacc3usr", email='hillary@actserv.com', firstname='Hillary', lastname='Juma', password="testpassword")

@pytest.fixture()
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    """  
    yield APIClient()

@pytest.fixture
def transaction_payload(inve
