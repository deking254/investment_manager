# test_views.py
import pytest
import logging
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from investmentmanager.models import Transaction
from django.contrib.auth.models import Permission

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

@pytest.mark.django_db
def test_get_accounts_unauthenticated(api_client):
    #get users without authentication
    response_get = api_client.get('/investmentaccounts/')
    assert response_get.status_code == 403

@pytest.mark.django_db
def test_get_transactions_authenticated(api_client, investmentacc1usr):
    # authenticate the user
    api_client.force_authenticate(user=investmentacc1usr)

    # send a get request with the authenticated user
    response_get = api_client.get('/transactions/', format="json")
    assert response_get.status_code == 200

@pytest.mark.django_db
def test_get_users_authenticated(api_client, investmentacc2usr):
    #authenticated use get users
    api_client.force_authenticate(user=investmentacc2usr)
    #send a get request with the authenticated user
    response_get = api_client.get('/users/', format="json")
    assert response_get.status_code == 200

@pytest.mark.django_db
def test_get_investmentaccounts_authenticated(api_client, investmentacc3usr):
    #authenticated use get investmentaccounts
    api_client.force_authenticate(user=investmentacc3usr)
    #send a get request with the authenticated user
    response_get = api_client.get('/investmentaccounts/', format="json")
    assert response_get.status_code == 200

@pytest.mark.django_db
def test_delete_users_authenticated(api_client, admin_user, investmentacc3usr):
    #authenticated use get investmentaccounts
    api_client.force_authenticate(user=admin_user)
    #send a get request with the authenticated user
    url = reverse('user-detail', args=[investmentacc3usr.id])
    response_get = api_client.delete(url)
    assert response_get.status_code == 204

@pytest.mark.django_db
def test_create_groups(create_groups):
    # Verify that three groups were created
    assert len(create_groups) == 3
    
    # Check if the groups exist in the database
    group_names = [group.name for group in create_groups]
    assert 'investmentacc1' in group_names
    assert 'investmentacc2' in group_names
    assert 'investmentacc3' in group_names

    # Check permissions for each group
    content_type = ContentType.objects.get_for_model(Transaction)
    permissions = Permission.objects.filter(content_type=content_type)
    for group in create_groups:
        if group.name == 'investmentacc1':
            view_permission = group.permissions.filter(codename='view_transaction', content_type=content_type).exists()
            add_permission = group.permissions.filter(codename='add_transaction', content_type=content_type).exists()
            change_permission = group.permissions.filter(codename='change_transaction', content_type=content_type).exists()
            delete_permission = group.permissions.filter(codename='delete_transaction', content_type=content_type).exists()
            assert view_permission
            assert not add_permission
            assert not change_permission
            assert not delete_permission
        if group.name == 'investmentacc2':
            view_permission = group.permissions.filter(codename='view_transaction', content_type=content_type).exists()
            add_permission = group.permissions.filter(codename='add_transaction', content_type=content_type).exists()
            change_permission = group.permissions.filter(codename='change_transaction', content_type=content_type).exists()
            delete_permission = group.permissions.filter(codename='delete_transaction', content_type=content_type).exists()
            assert view_permission
            assert add_permission
            assert change_permission
            assert delete_permission
        if group.name == 'investmentacc3':
            view_permission = group.permissions.filter(codename='view_transaction', content_type=content_type).exists()
            add_permission = group.permissions.filter(codename='add_transaction', content_type=content_type).exists()
            change_permission = group.permissions.filter(codename='change_transaction', content_type=content_type).exists()
            delete_permission = group.permissions.filter(codename='delete_transaction', content_type=content_type).exists()
            assert not view_permission
            assert add_permission
            assert not change_permission
            assert not delete_permission

