import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.authentik import authentik_common as c


def authentik_oidc_setup():
    # Get Flow UUID
    AUTH_FLOW_NAME = "default-provider-authorization-explicit-consent"
    INVALID_FLOW_NAME = "default-invalidation-flow"
    auth_flow_url = f"{c.AUTHENTIK_HOST}/api/v3/flows/instances/{AUTH_FLOW_NAME}/"
    invalid_flow_url = f"{c.AUTHENTIK_HOST}/api/v3/flows/instances/{INVALID_FLOW_NAME}/"
    auth_flow_uuid_resp = requests.get(auth_flow_url, verify=False, timeout=5, headers=c.AUTHENTIK_HEADER)
    auth_flow_uuid = auth_flow_uuid_resp.json()["pk"]
    print(auth_flow_uuid)

    invalid_flow_uuid_resp = requests.get(invalid_flow_url, verify=False, timeout=5, headers=c.AUTHENTIK_HEADER)
    invalid_flow_uuid = invalid_flow_uuid_resp.json()["pk"]
    print(invalid_flow_uuid)

    # Create oauth2 provider
    provider_oauth_url = f"{c.AUTHENTIK_HOST}/api/v3/providers/oauth2/"
    provider_oauth_payload = {
        "name": "vdiaas-oauth-provider",
        "authorization_flow": auth_flow_uuid,
        "invalidation_flow": invalid_flow_uuid,
        "client_type": "confidential",
        "client_id": "vdiaas-oauth-provider",
        "client_secret": "vdiaas-oauth-provider",
        "response_types": [
            "code",
            "token",
            "id_token"
        ],
        "grant_type": "password",
        "redirect_uris": [{
            "matching_mode": "strict",
            "url": "http://192.168.0.80:5173/signup"
        }]
    }
    provider_resp = requests.post(provider_oauth_url, json=provider_oauth_payload, verify=False, timeout=12, headers=c.AUTHENTIK_HEADER)
    provider_oauth_id = provider_resp.json()["pk"]
    print(provider_oauth_id)

    provider_oauth_patch_url = f"{c.AUTHENTIK_HOST}/api/v3/providers/oauth2/{provider_oauth_id}/"
    provider_oauth_patch_payload = {
        "authorization_grant_types": [
            "authorization_code",
            "password",
            "refresh_token"
        ]
    }
    provider_oauth_patch_response = requests.patch(provider_oauth_patch_url, headers=c.AUTHENTIK_HEADER, json=provider_oauth_patch_payload, verify=False, timeout=12)
    print(provider_oauth_patch_response.json())

    # Create Oauth Application URL
    oauth_app_url = f"{c.AUTHENTIK_HOST}/api/v3/core/applications/"
    oauth_app_payload = {
        "name": "VDIaaS Oauth APP",
        "slug": "vdiaas-oauth-app",
        "provider": provider_oauth_id,
        "meta_launch_url": "http://192.168.0.80:5173/signup"
    }
    oauth_app_resp = requests.post(oauth_app_url, json=oauth_app_payload, verify=False, timeout=12, headers=c.AUTHENTIK_HEADER)
    print(oauth_app_resp.json())
authentik_oidc_setup()

