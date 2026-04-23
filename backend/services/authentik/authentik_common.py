AUTHENTIK_HOST = "http://[authentik_ip:9000]"
PG_PASSWORD = "[db_password]"
AUTHENTIK_API_TOKEN = "[token]"
AUTHENTIK_HEADER = {
    "Authorization": f"Bearer {AUTHENTIK_API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
