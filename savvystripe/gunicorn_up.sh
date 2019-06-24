gunicorn --bind :8080  --log-syslog --error-logfile /srv/payments/savvystripe/savvystripe-errors.log ecommerce.wsgi -D

