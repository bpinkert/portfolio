#!/bin/bash
# 
#
# Openvpn setup script
sudo apt-get update
sudo apt-get install -y openvpn easy-rsa
#sudo make-cadir /etc/openvpn/cadir
#sudo cd /etc/openvpn/cardir
sudo cp -r /usr/share/easy-rsa /etc/openvpn
#sudo openssl dhparam -out /etc/openvpn/dh2048.pem 2048
sudo cat > /etc/openvpn/server.conf << EOF
local 0.0.0.0
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "dhcp-option DNS 208.67.222.222"
push "dhcp-option DNS 208.67.220.220"
keepalive 10 120
tls-auth ta.key 0 # This file is secret
key-direction 0
cipher AES-256-CBC
auth SHA256
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
log-append  /var/log/openvpn.log
verb 3
explicit-exit-notify 1
EOF

sudo cat /etc/openvpn/server.conf

#sudo gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz > /etc/openvpn/server.conf
# read -p 'KEY_COUNTRY: ' countryvar
# read -p 'KEY_PROVINCE: ' provincevar
# read -p 'KEY_CITY: ' cityvar
# read -p 'KEY_ORG: ' orgvar
# read -p 'KEY_EMAIL: ' emailvar
# read -p 'KEY_OU: ' ouvar
#sudo touch /etc/openvpn/easy-rsa/vars

sudo cat > /etc/openvpn/easy-rsa/vars << EOF
export EASY_RSA="/etc/openvpn/easy-rsa" 
export OPENSSL="openssl" 
export PKCS11TOOL="pkcs11-tool" 
export GREP="grep" 
export KEY_CONFIG="$EASY_RSA/whichopensslcnf $EASY_RSA" 
export KEY_DIR="$EASY_RSA/keys" 
export PKCS11_MODULE_PATH="dummy" 
export PKCS11_PIN="dummy" 
export KEY_SIZE=2048 
export CA_EXPIRE=3650 
export KEY_EXPIRE=3650 
export KEY_COUNTRY='US' 
export KEY_PROVINCE='CT' 
export KEY_CITY='Norwalk'
export KEY_ORG='Apex Technology Services' 
export KEY_EMAIL='support@apextechservices.com' 
export KEY_OU='IT' 
export KEY_NAME='server'
EOF

sudo cat /etc/openvpn/easy_rsa/vars

sudo echo 1 > /proc/sys/net/ipv4/ip_forward
oipv4f='#net.ipv4.ip_forward=1'
nipv4f='net.ipv4.ip_forward=1'
sudo sed -i -e "s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g" /etc/sysctl.conf
sudo ufw allow ssh
sudo ufw allow 1194/udp
sudo cat > /etc/default/ufw << EOF
# /etc/default/ufw
#
IPV6=yes
DEFAULT_INPUT_POLICY="DROP"
DEFAULT_OUTPUT_POLICY="ACCEPT"
DEFAULT_FORWARD_POLICY="ACCEPT"
DEFAULT_APPLICATION_POLICY="SKIP"
MANAGE_BUILTINS=no
IPT_SYSCTL=/etc/ufw/sysctl.conf
IPT_MODULES="nf_conntrack_ftp nf_nat_ftp nf_conntrack_netbios_ns"
EOF

sudo cat /etc/default/ufw

cd /etc/openvpn/easy-rsa
source ./vars
sudo ./clean-all
sudo ./build-ca
sudo ./build-key-server server
sudo openvpn --genkey --secret keys/ta.key 

cd /etc/openvpn/easy-rsa
source vars 
sudo ./build-key client1
cd /etc/openvpn/easy-rsa/keys
sudo cp ca.crt server.crt server.key ta.key /etc/openvpn