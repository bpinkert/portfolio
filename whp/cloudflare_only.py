import requests
import subprocess

cf_ip4_url = 'https://www.cloudflare.com/ips-v4'

ips = requests.get(cf_ip4_url)

ip_list = list()

for line in ips.text.split('\n'):
    if line == '':
        pass
    else:
        ip_list.append(line)

ufw_cmd = 'sudo ufw allow proto tcp from {} to any port 80,443'

for ip_range in ip_list:
    cmd = ufw_cmd.format(ip_range)
    s = subprocess.Popen(cmd, shell=True)
    s.wait()
