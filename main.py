import psutil
import time

KEYWORDS = [
    'Proton',
    'ProtonVPN',
    'Proton VPN',
    'ProtonVPN Service',
    'mullvad',
    'nord',
    'openvpn',
    'express',
    'surfshark',
    'cyberghost',
    'windscribe',
    'pia',
    'hotspot',
    'tunnelbear'
]

def kill_processes_by_keywords(keywords):
    keywords = [k.lower() for k in keywords]
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name']
            if pname and any(k in pname.lower() for k in keywords):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

for _ in range(5):
    kill_processes_by_keywords(KEYWORDS)
    time.sleep(1)

