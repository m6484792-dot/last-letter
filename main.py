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
    'wireguard',
    'tunnelbear'
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
        time.sleep(0.5)

kill_processes_by_keywords(KEYWORDS)
