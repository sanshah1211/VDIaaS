import httpx
import json

CLIENT_ID = "vdiaas-oauth-provider"
CLIENT_SECRET = "vdiaas-oauth-provider"
ISSUER_URL = "http://192.168.0.80:9000/application/o/vdiaas-oauth-app"
BACKEND_URL = "http://192.168.0.80:8000"
FRONTEND_URL = "http://192.168.0.80:5173"

metadata = httpx.get(f"{ISSUER_URL}/.well-known/openid-configuration").json()
authorization_url = metadata["authorization_endpoint"]
token_url = metadata["token_endpoint"]

print(authorization_url)
print(token_url)