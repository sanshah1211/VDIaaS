import requests
import psycopg2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.authentik import authentik_common as c

AUTH_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def authentik_token_setup(username, password):
    url = f"{c.AUTHENTIK_HOST}/api/v3/flows/executor/default-authentication-flow/"
    session = requests.Session()
    # Start flow
    user_session = session.get(url)
    print("Stage 1:", user_session.json())
    if username == "akadmin":
        # Identification stage
        payload = {
            "component": "ak-stage-identification",
            "uid_field": username
        }
        user_session = session.post(url, json=payload)
        print("Stage 2:", user_session.json())
        # Password stage
        payload = {
            "component": "ak-stage-password",
            "password": password
        }
        user_session = session.post(url, json=payload)
        print("Stage 3:", user_session.json())

        session_cookie = session.cookies.get("authentik_session")
        print("Session cookie:", session_cookie)

        device = session.cookies.get("authentik_device")

        # Get CSRF token
        csrf_token = session.cookies.get("authentik_csrf")
        print("CSRF token:", csrf_token)
        print("Session Cookies:", session.cookies)

        cookie_header = f"authentik_session={session_cookie}; authentik_csrf={csrf_token}"

        AUTH_HEADERS = {
            "Content-Type": "application/json",
            "X-authentik-CSRF": session.cookies.get("authentik_csrf"),
        }

        logged_in_url = f"{c.AUTHENTIK_HOST}/api/v3/core/users/me/"
        user_session = session.get(logged_in_url, verify=False)
        if user_session.status_code == 200:
            token_payload = {
                "identifier": "automation_token",
                "description": "Token created via API",
                "intent": "api",
                "user": 4,
                "expiring": False
            }

            token_url = f"{c.AUTHENTIK_HOST}/api/v3/core/tokens/"
            print(AUTH_HEADERS)
            resp = session.post(token_url, json=token_payload, headers=AUTH_HEADERS,verify=False)
            if resp.status_code == 201:
                print("Token created:", resp.json())
                conn = psycopg2.connect(database = "authentik",
                                        user = "authentik",
                                        host = 'localhost',
                                        port = 5431,
                                        password = c.PG_PASSWORD
                                        )
                cur = conn.cursor()
                cur.execute("SELECT key FROM authentik_core_token WHERE identifier = 'automation_token';")
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                AUTHENTIK_API_TOKEN = rows[0][0]
                print(AUTHENTIK_API_TOKEN)
                common_settings = "./authentik_common.py"
                with open(common_settings, "r") as f:
                    lines = f.readlines()

                with open(common_settings, "w") as f:
                    for line in lines:
                        if line.startswith("AUTHENTIK_API_TOKEN"):
                            f.write(f'AUTHENTIK_API_TOKEN = "{AUTHENTIK_API_TOKEN}"\n')
                        else:
                            f.write(line)

            else:
                print("Error:", resp)
authentik_token_setup(username="akadmin", password="redhat123")