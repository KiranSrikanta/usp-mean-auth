__author__ = 'administrator'

import requests

# HARD CODED!!!
vra_url = "https://vcac1.rideblr.com/"
vra_user_name = "administrator@rideblr.com"
vra_password = "VMware1!"
# Default tenant name
vra_tenant_name = "vsphere.local"


def create_request(request_message):

    # Call REST endpoint and update request id.
    auth_token = auth_vra()

    catalog_item = get_catalog_item_by_id(request_message['Service'], auth_token)

    vm_req_json = {
        "@type": "CatalogItemRequest",
        "catalogItemRef": {
            "id": catalog_item['catalogItem']['id']
        },
        "organization": {
            "tenantRef": vra_tenant_name,
            "subtenantRef": catalog_item['entitledOrganizations'][0]['subtenantRef']
        },
        "requestedFor": vra_user_name,
        "state": "SUBMITTED",
        "requestNumber": 0,
        "requestData": {
            "entries": [
                {
                    "key": "provider-blueprintId",
                    "value": {
                        "type": "string",
                        "value": catalog_item['catalogItem']['providerBinding']['bindingId']
                    }
                },
                {
                    "key": "provider-provisioningGroupId",
                    "value": {
                        "type": "string",
                        "value": catalog_item['entitledOrganizations'][0]['subtenantRef']
                    }
                },
                {
                    "key": "requestedFor",
                    "value": {
                        "type": "string",
                        "value": vra_user_name
                    }
                }
            ]
        }
        }

    response = requests.request(method='post', url=vra_url + '/catalog-service/api/consumer/requests', verify=False,
                                headers={'Content-Type': 'application/json',
                                         'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + auth_token},
                                json=vm_req_json)

    request_message['RequestId'] = response.headers['Location'].rsplit(sep="/requests/")[1]
    return request_message


def auth_vra():
    response = requests.request(method='post', url=vra_url + '/identity/api/tokens', verify=False, json={
        "username": vra_user_name,
        "password": vra_password,
        "tenant": vra_tenant_name})

    response_json = response.json()
    return response_json['id']


def get_catalog_item_by_id(catalog_item_id, auth_token):
    if auth_token is None:
        auth_token = auth_vra()

    response = requests.request(method='get', url=vra_url + "/catalog-service/api/consumer/entitledCatalogItems/" +
                                                            catalog_item_id,
                                headers={'Content-Type': 'application/json',
                                         'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + auth_token},
                                verify=False)
    catalog_item = response.json()
    return catalog_item


def get_request_by_id(request_id, auth_token):
    if auth_token is None:
        auth_token = auth_vra()

    response = requests.request(method='get', url=vra_url + "/catalog-service/api/consumer/requests/" +
                                                            request_id,
                                headers={'Content-Type': 'application/json',
                                         'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + auth_token},
                                verify=False)
    request_json = response.json()
    return request_json

