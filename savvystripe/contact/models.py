from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site
from django.db.models import signals
from notifications import models as notification
import subprocess
# Create your models here.

# def create_notice_types(app, created_models, verbosity, **kwargs):
#     notification.create_notice_type("new_comment", "Comment posted", "A comment has been posted")
# signals.post_syncdb.connect(create_notice_types, sender=notification)

def whois(domain):     
    answer = subprocess.Popen(['whois', domain], stdout=subprocess.PIPE).communicate()          
    return answer  



def new_comment(sender, instance, created, **kwargs):
    # remove this if-block if you want notifications for comment edit too
    if not created:
        return None

    context = {
        'comment': instance,
        'site': Site.objects.get_current(),
    }
    recipients = []

    # add all users who commented the same object to recipients
    for comment in instance.__class__.objects.for_model(instance.content_object):
        if comment.user not in recipients and comment.user != instance.user:
            recipients.append(comment.user)

    # if the commented object is a user then notify him as well
    if isinstance(instance.content_object, models.get_model('auth', 'User')):
        # if he his the one who posts the comment then don't add him to recipients
        if instance.content_object != instance.user and instance.content_object not in recipients:
            recipients.append(instance.content_object)

    notification.send(recipients, 'new_comment', context)

signals.post_save.connect(new_comment, sender=('comments', 'Comment'))