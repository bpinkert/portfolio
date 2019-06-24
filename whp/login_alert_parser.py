#!/usr/bin/env python
import sys
import imaplib
# import getpass
import email
import email.header
import datetime
import argparse
import csv
import os

# import xlsxwriter

EMAIL_ACCOUNT = ""
EMAIL_FOLDER = ""

M = imaplib.IMAP4_SSL('outlook.office365.com')


def parsed_to_csv(parsed):
    """

    :param parsed: list of dict objects
    :return:
    """
    csv_columns = ['Date', 'Subject', 'Account Name', 'Account Domain', 'Logon Account Name', 'Logon Domain Name',
                   'Logon Type', 'Caller Process', 'Workstation Name', 'Source Network Address', 'Source Port',
                   'Authentication Package', 'Raw']
    # current_path = os.getcwd()
    # csv_file = current_path + "\\Windows_Logon_Failures.csv"
    a_drive = os.path.abspath('A:')
    p = a_drive + '\\Processes\\Windows_Logon_Failures.csv'
    csv_file = os.path.abspath(p)
    try:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator='\n')
            # writer.writeheader()
            for data in parsed:
                writer.writerow(data)
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))
    return


def parse_messages(message_list):
    """
    Takes the message list filled with MIME email objects
    and parses into another list of dict objects

    :param message_list: list of MIME emails
    :return: parsed_list: list of dict objects
    """
    parsed_list = list()
    for msg in message_list:
        message_dict = dict()
        body = msg.get_payload(decode=True)
        message_dict['Raw'] = body.replace('\r\n', '')

        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            message_dict['Date'] = local_date
        message_dict['Subject'] = msg['Subject']
        alert = body.split('message:')[1]
        alert = alert.replace('\r\n', '')
        account_name = alert.split('Account Name:')[1].split('Account Domain:')[0].strip(' ')
        if account_name:
            message_dict['Account Name'] = account_name
        account_domain = alert.split('Account Domain:')[1].split('Logon ID:')[0].strip(' ')
        if account_domain:
            message_dict['Account Domain'] = account_domain
        logon_account_name = alert.split('Account Name:')[2].split('Account Domain:')[0].strip(' ')
        if logon_account_name:
            message_dict['Logon Account Name'] = logon_account_name
        logon_domain_name = alert.split('Account Domain:')[2].split('Failure Information:')[0].strip(' ')
        if logon_domain_name:
            message_dict['Logon Domain Name'] = logon_domain_name
        logon_type = alert.split('Logon Type:')[1].split('Account For Which Logon Failed:')[0].strip(' ')
        if logon_type:
            message_dict['Logon Type'] = logon_type
        caller_process = alert.split('Caller Process Name:')[1].split('Network Information:')[0].strip(' ')
        if caller_process:
            message_dict['Caller Process'] = caller_process
        workstation_name = alert.split('Workstation Name:')[1].split('Source Network Address:')[0].strip(' ')
        if workstation_name:
            message_dict['Workstation Name'] = workstation_name
        source_network_address = alert.split('Source Network Address:')[1].split('Source Port:')[0].strip(' ')
        if source_network_address:
            message_dict['Source Network Address'] = source_network_address
        source_port = alert.split('Source Port:')[1].split('Detailed Authentication Information:')[0].strip(' ')
        if source_port:
            message_dict['Source Port'] = source_port
        auth_package = alert.split('Authentication Package:')[1].split('Transited Services:')[0].strip(' ')
        if auth_package:
            message_dict['Authentication Package'] = auth_package
        parsed_list.append(message_dict)

    return parsed_list


def process_mailbox(M, **kwargs):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """
    message_list = list()

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        message_list.append(msg)
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")
        if 'delete' in kwargs:
            M.store(num, '+FLAGS', '\\Deleted')
            print "***Deleting email***"
    return message_list


def connect_mailbox(M, pw, **kwargs):
    try:
        # alert_pass = getpass.getpass()
        # rv, data = M.login(EMAIL_ACCOUNT, alert_pass)
        rv, data = M.login(EMAIL_ACCOUNT, pw)
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!!! "
        sys.exit(1)

    print rv, data

    rv, mailboxes = M.list()
    if rv == 'OK':
        print "Mailboxes:"
        print mailboxes

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print "Processing mailbox...\n"
        if 'delete' in kwargs:
            mail = process_mailbox(M, delete=True)
            M.close()
            return mail
        else:
            mail = process_mailbox(M)
            M.close()
            return mail
    else:
        print "ERROR: Unable to open mailbox ", rv

    M.logout()


def main():
    parser = argparse.ArgumentParser(add_help=True, prog='python script to check Windows Logon Alerts via IMAP',
                                     description="python script to check Windows Logon Alerts via IMAP",
                                     usage='Use like so: python login_alert_parser.py -p <password> add -d or --delete '
                                           'if you want to delete the messages read')

    parser.add_argument('-p', '--password', action='store', dest='password', help='-p <password>')
    parser.add_argument('-d', '--delete', action='store_true', dest='delete', default=False,
                        help='--delete or -d')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()
    pw = str(options.password)
    delete = options.delete

    if options.password is None:
        print "Password required use the -p switch"
        sys.exit(1)

    if delete is False:
        try:
            message_list = connect_mailbox(M, pw)
            parsed = parse_messages(message_list)
            parsed_to_csv(parsed)
        except Exception as e:
            print "Error: %e" % e
    else:
        try:
            message_list = connect_mailbox(M, pw, delete=True)
            parsed = parse_messages(message_list)
            parsed_to_csv(parsed)
            # connect_mailbox(M, pw, delete=True)
        except Exception as e:
            print "Error: %e" % e


if __name__ == '__main__':
    main()
