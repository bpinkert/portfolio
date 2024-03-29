#!/bin/bash

# $countryvar=US
# $provincevar=CT
# $cityvar=Norwalk
# $orgvar=Apex
# $emailvar=bpinkert@apextechservices.com
# $ouvar=IT

cat > /etc/openvpn/cadir/vars << EOF
export EASY_RSA="`pwd`" 
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
export KEY_PROVINCE='US' 
export KEY_CITY='US'
export KEY_ORG='US' 
export KEY_EMAIL='US' 
export KEY_OU='US' 
export KEY_NAME='EasyRSA'
EOF

cat /etc/openvpn/cadir/vars

