#!/usr/bin/env python
#
import argparse
import requests
import json

api_key = ''


class Campaign:
    def __init__(self, campaign_id, name, created_date, completed_date, template, page, status, results, timeline, smtp,
                 campaign_url):
        self.campaign_id = campaign_id
        self.name = name
        self.created_date = created_date
        self.completed_date = completed_date
        self.template = template
        self.page = page
        self.status = status
        self.results = results
        self.timeline = timeline
        self.smtp = smtp
        self.campaign_url = campaign_url

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def parse_datetime(time):
    # convert 2018-05-24T16:27:12.220026189Z to 5-24-2017 16:27:12
    t = time.rsplit('Z')[0]
    t = t.rsplit('.')
    mil_time = t[0].split('T')[1]
    date = t[0].split('T')[0]
    month = date.split('-')[1]
    day = date.split('-')[2]
    year = date.split('-')[0]
    datetime = month + '-' + day + '-' + year + ' ' + mil_time + ' EST'

    return datetime


def writefile(campaign):
    """
    Generates the report in html and writes to html file.
    """
    # formatting the email in html.

    styles = """
 #phishing-header {
    font-size: 2.5rem;
    margin-bottom: .5rem;
    font-family: inherit;
    font-weight: 500;
    line-height: 1.2;
    color: inherit;
    margin-top: 0;
    }
 #footnote {
    padding-top: 40px;
    font-weight: bold;
    padding-bottom: 40px;
    }
 body {
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,
    "Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol" !important;
    }
 .table-bordered td, .table-bordered th {
    border: 1px solid #dee2e6;
    border-bottom-color: rgb(222, 226, 230);
    border-bottom-style: solid;
    border-bottom-width: 1px;
    }
 .table td, .table th {
    padding: .75rem;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
    }
 .btn-link {
    font-weight: 400;
    color: #007bff;
    background-color: transparent;
    }
 .btn {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    border: 1px solid transparent;
    padding: .375rem .75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: .25rem;
    transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow 
    .15s ease-in-out;
    }
 .table-bordered {
    border: 1px solid #dee2e6;
    }
 .table {
    width: 100%;
    max-width: 100%;
    margin-bottom: 1rem;
    background-color: transparent;
    }         
    """

    reporthtml = "<!doctype html>"
    reporthtml += "<html lang='en'>\n" \
                  "<head profile=\"http://www.w3.org/2005/10/profile\">\n" \
                  "<link rel=\"icon\" href=\"https://www.apextechservices.com/favicon.ico\">" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"57x57\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"60x60\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"72x72\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"76x76\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"114x114\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"120x120\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"144x144\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"152x152\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link href=\"https://www.apextechservices.com/favicon.ico\" sizes=\"180x180\" " \
                  "rel=\"apple-touch-icon\">\n" \
                  "<link sizes=\"32x32\" href=\"https://www.apextechservices.com/favicon.ico\" " \
                  "type=\"image/png\" rel =\"icon\" >\n" \
                  "<link sizes=\"194x194\" href=\"https://www.apextechservices.com/favicon.ico\" " \
                  "type=\"image/png\" rel=\"icon\" >\n" \
                  "<link sizes=\"96x96\" href=\"https://www.apextechservices.com/favicon.ico\" " \
                  "type=\"image/png\" rel=\"icon\" >\n" \
                  "<link sizes=\"192x192\" href=\"https://www.apextechservices.com/favicon.ico\" " \
                  "type=\"image/png\" rel=\"icon\" >\n" \
                  "<link sizes=\"16x16\" href=\"https://www.apextechservices.com/favicon.ico\" " \
                  "type=\"image/png\" rel=\"icon\" >\n"
    reporthtml += "<link rel=\"stylesheet\" " \
                  "href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css\" " \
                  "integrity=\"sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB\" " \
                  "crossorigin=\"anonymous\">\n"
    reporthtml += "<meta http-equiv='Content-Type' content='text/html' charset='utf-8' />\n"
    reporthtml += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">\n"
    reporthtml += "<title>%s </title>" % str(campaign.name)
    reporthtml += "\n<link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.1.0/css/all.css\" " \
                  "integrity=\"sha384-lKuwvrZot6UHsBSfcMvOkWwlCMgc0TaWr+30HWe3a4ltaBwTZhyTEggF5tJv8tbt\" " \
                  "crossorigin=\"anonymous\">\n</head>\n<body>\n" \
                  "<div class=\"container-fluid col-md-10 col-md-offset-2\">\n<div>\n"
    reporthtml += "<style>{}</style>".format(styles)
    reporthtml += "<p class=\"text-center\">\n<a href=\"https://www.apextechservices.com\">\n" \
                  "<img src=\"https://images.tmcnet.com/tmc/vertical/apex/images/apex-reg-logo.gif\" /></a></p>\n"
    reporthtml += "<p class=\"text-center\">535 Connecticut Ave. Suite 104 Norwalk CT 06854 - 203-295-5050</p>\n"
    reporthtml += "<hr>\n<h1 class=\"text-center\" id=\"phishing-header\">Phishing Campaign Results</h1>\n"
    reporthtml += "<table class=\"table table-striped table-bordered table-hover \">\n"
    reporthtml += "<thead>\n<tr>\n<th colspan=\"3\" class=\"text-center\"> Campaign ID: "\
                  + str(campaign.campaign_id) + "&nbsp;&nbsp;&nbsp;  Campaign Name: " + str(campaign.name)
    reporthtml += "</th>\n</tr>\n<tr>\n<th class=\"text-center\">Campaign status: " + str(campaign.status) \
                  + "<br></th>\n<th class=\"text-center\"> Created: " + parse_datetime(campaign.created_date) + \
                  "<br></th>\n<th class=\"text-center\"> Completed: " + parse_datetime(campaign.completed_date) + \
                  "</th>\n</tr>\n</thead>\n</table>"

    timeline_html = "<table class=\"table table-striped table-sm\">" \
                    "<thead><tr>" \
                    "<th>Event</th>" \
                    "<th>Email</th>" \
                    "<th>Date / Time</th>" \
                    "</tr>" \
                    "</thead>" \
                    "<tbody>"

    for event in campaign.timeline:
        event_message = str(event['message'])
        if len(event['email']) is 0:
            event_email = "N/A"
        else:
            event_email = str(event['email'])
        event_time = parse_datetime(event['time'])
        if event_message == "Submitted Data":
            eventhtml = "<tr>\n" \
                        "<td class=\"alert-danger\" width=\"30%\">{}</td>\n" \
                        "<td width=\"30%\">{}</td>\n" \
                        "<td width=\"30%\">{}</td>\n" \
                        "</tr>" \
                        .format(event_message, event_email, event_time)
        elif event_message == "Clicked Link":
            eventhtml = "<tr>\n" \
                        "<td class=\"alert-warning\" width=\"30%\">{}</td>\n" \
                        "<td width=\"30%\">{}</td>\n" \
                        "<td width=\"30%\">{}</td>\n" \
                        "</tr>" \
                        .format(event_message, event_email, event_time)
        else:
            eventhtml = "<tr>\n" \
                "<td width=\"30%\">{}</td>\n" \
                "<td width=\"30%\">{}</td>\n" \
                "<td width=\"30%\">{}</td>\n" \
                "</tr>" \
                .format(event_message, event_email, event_time)
        timeline_html += eventhtml + "\n\n"

    timeline_html += "</tbody></table>"

    # loop through each result
    resulthtml = "<table class=\"table table-striped table-sm\">" \
                 "<thead><tr>" \
                 "<th>Event Status</th>" \
                 "<th>Name</th>" \
                 "<th>Position</th>" \
                 "<th>Email</th>" \
                 "<th>IP Address</th>" \
                 "<th>User Unique ID</th>" \
                 "</tr>" \
                 "</thead>" \
                 "<tbody>"
    for result in campaign.results:
        result_id = result['id']
        result_status = result['status']
        result_fullname = result['first_name'] + ' ' + result['last_name']
        result_position = result['position']
        if len(result_position) is 0:
            result_position = "N/A"
        else:
            result_position = result['position']
        result_email = result['email']
        result_ip = result['ip']
        if result_status == "Submitted Data":
            resulthtml += "<tr>\n" \
                          "<td class=\"alert-danger\" width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "</tr>".format(result_status,
                                         result_fullname,
                                         result_position,
                                         result_email,
                                         result_ip,
                                         result_id)
        elif result_status == "Clicked Link":
            resulthtml += "<tr>\n" \
                          "<td class=\"alert-warning\" width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "</tr>".format(result_status,
                                         result_fullname,
                                         result_position,
                                         result_email,
                                         result_ip,
                                         result_id)
        else:
            resulthtml += "<tr>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "<td width=\"15%\">{}</td>\n" \
                          "</tr>".format(result_status,
                                         result_fullname,
                                         result_position,
                                         result_email,
                                         result_ip,
                                         result_id)

    resulthtml += "\n</tbody>" \
                  "\n</table>" \

    # add email template
    emailhtml = "<div>"
    emailhtml += "<h3 class=\"text-center\">Email Template:</h3><p><b>Email From Display Name:</b> {}</p>" \
                 "<br><p><b>Email From Address:</b> {}</p><br><p><b>Email Subject:</b> {}</p>{}".format(
                                                           campaign.smtp['from_address'].split('<')[0],
                                                           campaign.smtp['from_address'].split('<')[1].rsplit('>')[0],
                                                           campaign.template['subject'],
                                                           campaign.template['html'].rsplit('{{.Tracker}}')[0].encode(
                                                               'ascii', 'ignore').decode('ascii'))
    emailhtml += "</div>"
    # add the landing page template
    emailhtml += "<div>"
    redirect_url = campaign.page['redirect_url'].encode('ascii', 'ignore').decode('ascii')
    page_html = campaign.page['html'].encode('ascii', 'ignore').decode('ascii')

    pagehtml = "<h3 class=\"text-center\">Landing Page Template:</h3><br><p><b>Redirect to url on form submit:</b> " \
               "{}</p><p style=\"border-top-style: solid;border-top-width: 2px;margin-top: 25px;\">{}</p>".format(
                redirect_url, page_html)
    pagehtml += "</div>"
    reporthtml += """
<div class=\"accordion\" id=\"accordion\">
    <div class=\"card\">
        <div class=\"card-header\" id=\"headingOne\">
        <h5 class=\"mb-0\">
        <button class=\"btn btn-link collapsed\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapseOne\" 
            aria-expanded=\"true\" aria-controls=\"collapseOne\">
            <i class="far fa-envelope fa-2x"></i> Click to view Email Template
        </button>
            </h5>
        </div>
        <div id=\"collapseOne\" class=\"collapse\" aria-labelledby=\"headingOne\" data-parent=\"#accordion\">
            <div class=\"card-body\">
            {}
            </div>
        </div>
  </div>
    <div class=\"card\">
        <div class=\"card-header\" id=\"headingTwo\">
        <h5 class=\"mb-0\">
        <button class=\"btn btn-link collapsed\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapseTwo\" 
            aria-expanded=\"false\" aria-controls=\"collapseTwo\">
            <i class="fas fa-file fa-2x"></i> Click to view Landing Page Template
        </button>
        </h5>
        </div>
        <div id=\"collapseTwo\" class=\"collapse\" aria-labelledby=\"headingTwo\" data-parent=\"#accordion\">
            <div class=\"card-body\">
            {}
            </div>
        </div>
    </div>
    <div class=\"card\">
        <div class=\"card-header\" id=\"headingThree\">
        <h5 class=\"mb-0\">
        <button class=\"btn btn-link collapsed\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapseThree\" 
            aria-expanded=\"false\" aria-controls=\"collapseThree\">
            <i class="fas fa-info fa-3x" style="padding-left:4px"></i></i> &nbsp;Click to view truncated results
        </button>
        </h5>
        </div>
        <div id=\"collapseThree\" class=\"collapse\" aria-labelledby=\"headingThree\" data-parent=\"#accordion\">
            <div class=\"card-body\">
            {}
            </div>
        </div>
        </div>
    <div class=\"card\">
        <div class=\"card-header\" id=\"headingFour\">
        <h5 class=\"mb-0\">
        <button class=\"btn btn-link collapsed\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapseFour\" 
            aria-expanded=\"false\" aria-controls=\"collapseFour\" style=\"padding-left:9px\">
            <i class="fas fa-clock fa-2x"></i></i>&nbsp;Click to view event timeline
        </button>
        </h5>
        </div>
        <div id=\"collapseFour\" class=\"collapse\" aria-labelledby=\"headingFour\" data-parent=\"#accordion\">
        <div class=\"card-body\">
        {}
        </div>
    </div>
  </div>
 </div>
    """.format(emailhtml, pagehtml, resulthtml, timeline_html)

    reporthtml += "<script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" " \
        " integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\"" \
        " crossorigin=\"anonymous\"></script>"
    reporthtml += "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js\"" \
        " integrity=\"sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49\"" \
        " crossorigin=\"anonymous\"> </script>"
    reporthtml += "<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js\" " \
        " integrity=\"sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T\" " \
        " crossorigin =\"anonymous\"> </script>"
    # add some CSS before closing the body

    # closing tags for the page
    reporthtml += "</div></div></body>" \
                  "<p class=\"text-center\" id=\"footnote\">If you have any questions please feel free to email " \
                  "<a href=\"mailto:support@apextechservices.com\">support@apextechservices.com</a></p>" \
                  "</html>"

    # write the report to file
    fname = "phishing-campaign-report-id-%s" % str(campaign.campaign_id)
    fname = fname + ".html"
    f = open(fname, "w")
    f.write(reporthtml)
    f.close()


def parse_campaign(campaign_id):

    req_url = 'https://security.outlookservicecenter.com:3333/api/campaigns/%s?api_key=%s' % (campaign_id, api_key)
    r = requests.get(req_url)
    data = r.text
    j = json.loads(data)
    campaign_id = j['id']
    name = j['name']
    created_date = j['created_date']
    completed_date = j['completed_date']
    template = j['template']
    page = j['page']
    status = j['status']
    results = j['results']
    timeline = j['timeline']
    smtp = j['smtp']
    campaign_url = j['url']
    c = Campaign(campaign_id,
                 name,
                 created_date,
                 completed_date,
                 template,
                 page,
                 status,
                 results,
                 timeline,
                 smtp,
                 campaign_url)

    return c


def main():

    parser = argparse.ArgumentParser(add_help = True, prog='python script to grab gophish campaign events and print '
                                                           'out html report',
                                     description = "python script to grab gophish campaign events",
                                     usage='Use like so: python gophish_report.py '
                                           '--id 68')

    parser.add_argument('--id', action='store', dest='id', help='raw.txt')
    options = parser.parse_args()
    camp_id = options.id

    if camp_id is None:
        print parser.print_usage()
        print "Campaign ID is blank. use --id number or absolute path"
    else:
        try:
            c = parse_campaign(camp_id)
            writefile(campaign=c)
        except Exception as e:
            print parser.print_usage()
            print "Unable to parse events with this ID"
            print "Exception: %s" % e


if __name__ == '__main__':
    main()
