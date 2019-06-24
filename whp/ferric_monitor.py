#!/usr/bin/env python
import subprocess
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import datetime

log_file = '/var/log/py_monitor.log'


def check_vpn_running():
    s = subprocess.Popen(['ps aux | grep openfortivpn | grep -v "grep"'],
                         shell=True, stdout=subprocess.PIPE)
    r = s.communicate()
    result = r[0]
    try:
        if result.split('./openfortivpn')[0] and result.split('./openfortivpn')[1] == ' -c ferric-config\n':
            f = open(log_file, 'a')
            now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
            f.write('{0} - VPN is running\n'.format(now))
            f.close()
            return True
        else:
            f = open(log_file, 'a')
            now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
            f.write('{0} - VPN is not running, restarting\n'.format(now))
            f.close()
            os.chdir('/root/openfortivpn/')
            subprocess.Popen(['./openfortivpn', '-c', 'ferric-config'], stdout=subprocess.PIPE)
            return True
    except Exception as e:
        f = open(log_file, 'a')
        now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
        f.write('{0} - VPN is not running, restarting\n'.format(now))
        f.close()
        os.chdir('/root/openfortivpn/')
        try:
            subprocess.Popen(['./openfortivpn', '-c', 'ferric-config'], stdout=subprocess.PIPE)
        except Exception as e:
            f = open(log_file, 'a')
            now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
            f.write('{0} - VPN can\'t reconnect to server, error: {}\n'.format(now, e))
            f.close()
        return False


def is_host_running(host):
    p1 = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    output = output.split('\n')
    if output[1].startswith('64 bytes from') and output[2].startswith('64 bytes from'):
        f = open(log_file, 'a')
        now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
        f.write('{0} - {1} is returning packets\n'.format(now, host))
        f.close()
        return True
    if output[-3].split(',')[2] == ' 100% packet loss':
        f = open(log_file, 'a')
        now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
        f.write('{0} - {1} is not returning any packets\n'.format(now, host))
        f.close()
        return False
    else:
        f = open(log_file, 'a')
        now = datetime.datetime.now().strftime('%m/%d/%y %H:%M')
        f.write('{0} - {1} is returning some packets but experiencing packet loss\n'.format(now, host))
        f.close()
        return "Not returning packets, but not experiencing 100% packet loss"


def email_support(subject, message):
    smtp_server = smtplib.SMTP('smtp.office365.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login('', '')
    msg = MIMEMultipart()

    fromaddr = ""
    toaddr = ""
    msg['From'] = ''
    msg['To'] = ''
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    smtp_server.sendmail(fromaddr, toaddr, text)
    smtp_server.quit()


def main():
    v = check_vpn_running()
    if v is True:
        first = is_host_running('amsterdam.ferricsemi.com')
        second = is_host_running('broadway.ferricsemi.com')
        if first is True:
            pass
        if second is True:
            pass
        if first is False:
            email_support('amsterdam.ferricsemi.com down', 'Ping tests show that amsterdam is showing 100% packet loss')
        if second is False:
            email_support('broadway.ferricsemi.com down', 'Ping tests show that broadway is showing 100% packet loss')
        # if first is "Not returning packets, but not experiencing 100% packet loss":
        #     email_support('amsterdam.ferricsemi.com packet loss',
        #                   'Ping tests show that amsterdam is showing packet loss')
        # if second is "Not returning packets, but not experiencing 100% packet loss":
        #     email_support('amsterdam.ferricsemi.com packet loss',
        #                   'Ping tests show that amsterdam is showing packet loss')
    else:
        email_support('ferric VPN down', 'unable to connect to ferric VPN')
        try:
            check_vpn_running()
            time.sleep(5)
            first = is_host_running('amsterdam.ferricsemi.com')
            second = is_host_running('broadway.ferricsemi.com')
            if first is True:
                pass
            if second is True:
                pass
            if first is False:
                email_support('amsterdam.ferricsemi.com down',
                              'Ping tests show that amsterdam is showing 100% packet loss')
            if second is False:
                email_support('broadway.ferricsemi.com down',
                              'Ping tests show that broadway is showing 100% packet loss')
        except Exception as e:
            email_support('ferric VPN down', 'unable to connect to ferric VPN twice in a row. error is {}'.format(e))
        # if first is "Not returning packets, but not experiencing 100% packet loss":
        #     email_support('amsterdam.ferricsemi.com packet loss',
        #                   'Ping tests show that amsterdam is showing packet loss')
        # if second is "Not returning packets, but not experiencing 100% packet loss":
        #     email_support('amsterdam.ferricsemi.com packet loss',
        #                   'Ping tests show that amsterdam is showing packet loss')


if __name__ == "__main__":
    main()
