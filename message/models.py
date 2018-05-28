# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='msg_sender')
    receiver = models.ForeignKey(User, related_name='msg_receiver')
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0}'.format(self.message)

    class Meta:
        ordering = ('sent_on',)
