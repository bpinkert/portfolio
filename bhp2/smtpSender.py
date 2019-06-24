#!/usr/env/python
import smtplib
from email.mime.text import MIMEText

host=''
port=587
user = ''
pwd = ''

def sendMail(user,pwd,to,subject,text):
	msg = MIMEText(text)
	msg['From'] = user
	msg['To'] = to
	msg['Subject'] = subject
	try:
	    smtpServer = smtplib.SMTP(host, port)
	    print "[+] Connecting To Mail Server."
	    smtpServer.ehlo()
	    print "[+] Starting Encrypted Session."
	    smtpServer.starttls()
	    smtpServer.ehlo()
	    print "[+] Logging into Mail Server."
	    smtpServer.login(user, pwd)
	    print "[+] Sending Mail."
	    smtpServer.sendmail(user, to, msg.as_string())
	    smtpServer.close()
	    print "[+] Mail Sent Successfully."
	except:
	    print "[-] Sending Mail Failed."

sendMail(user, pwd, 'bpinkert@websitesavants.com', 'Re: Mail send test', 'Test Message')
