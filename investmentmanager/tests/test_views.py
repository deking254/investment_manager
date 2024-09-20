# test_views.py
import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_get_transactions_unauthenticated(api_client):
    #get transactions
    response_get = api_client.get('/transactions/')
    assert response_get.status_code == 403

@pytest.mark.django_db
def test_get_users_unauthenticated(api_client):
    #get users without authentication
    response_get = api_client.get('/users/')
    assert response_get.status_code == 403
