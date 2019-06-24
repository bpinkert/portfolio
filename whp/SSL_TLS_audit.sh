#!/usr/bin/env bash
# OpenSSL requires the port number.
SERVER=$1
PORT=$2
DELAY=1
echo Testing all SSL/TLS versions at $1:$2 
echo Testing for SSLv3
ssl3command = "openssl s_client -connect $1:$2 -ssl3"
if [[ "$ssl3command" =~ ":error:" ]] ; then
  error=$(echo -n $ssl3command | cut -d':' -f6)
  echo NO \($error\)
else
  if [[ "$ssl3command" =~ "no peer certificate available" || "$result" =~ "Secure Renegotiation IS NOT supported" ]] ; then
    echo NO
  else
    echo YES
    echo $ssl3command
  fi
fi

# for cipher in ${ciphers[@]}
# do
# echo -n Testing $cipher...
# result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER 2>&1)
# if [[ "$result" =~ ":error:" ]] ; then
  # error=$(echo -n $result | cut -d':' -f6)
  # echo NO \($error\)
# else
  # if [[ "$result" =~ "Cipher is ${cipher}" || "$result" =~ "Cipher    :" ]] ; then
    # echo YES
  # else
    # echo UNKNOWN RESPONSE
    # echo $result
  # fi
# fi
# sleep $DELAY
# done