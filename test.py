import requests

AUTHENTIK_URL = "http://192.168.0.80:8000/api/v3/core/groups/"
TOKEN = "xdTSifCuR2Vok6FJ96NnDnmv77ed4LK5YdxmIVPvULBRtq8cIytvNmfy48vM"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def get_user_created_groups():
    response = requests.get(AUTHENTIK_URL, headers=headers)
    data = response.json()

    user_groups = []

    for group in data.get("results", []):
        # 🔥 Filtering logic
        if not group.get("is_superuser") and \
           not group.get("name", "").startswith("ak-") and \
           not group.get("attributes", {}).get("managed", False):

            user_groups.append({
                "name": group["name"],
                "pk": group["pk"]
            })

    return user_groups
