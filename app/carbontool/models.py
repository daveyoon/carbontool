# -*- encoding: utf-8 -*-

import os
from datetime import datetime

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):

    from django.db import models

    class Work(models.Model):
        json = models.TextField(default='[]')

        @staticmethod
        def get_by_id(id):
            return Work.objects.get(pk=id)

        def put(self):
            self.save()

        def unique_id(self):
            return self.id

    class Error(models.Model):
        error = models.TextField(default='')
        when = models.DateTimeField(default=datetime.now)

        @staticmethod
        def track(log):
            Error(error=log).save();

        @staticmethod
        def count(since=None):
            o = Error.objects
            if since:
                o = o.filter(when__gt=since)
            return o.count()

        @staticmethod
        def latest(items=10, since=None):
            q = Error.objects
            if since:
                q = q.filter(when__gt=since)
            return q.order_by('-when')[:items]

else:
    from models_appengine import *

