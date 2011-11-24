# -*- encoding: utf-8 -*-

import os
from datetime import datetime
import hashlib
import time 

try:
    import json
except:
    import simplejson as json

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

    class ErrorSummary(models.Model):
        key = models.CharField(max_length=128)
        error = models.TextField(default='')
        times = models.IntegerField(default=0)
        last_time = models.DateTimeField(default=datetime.now)
        #info_json =  models.TextField(default='{"times": 0, "ua": []')

        def timestamp(self):
            return time.mktime(self.last_time.timetuple())

        def to_dict(self):
            return {
                'date': self.timestamp() , 
                'error': json.loads(self.error),
                'times': self.times
            }

    class Error(models.Model):
        error = models.TextField(default='')
        when = models.DateTimeField(default=datetime.now)

        @staticmethod
        def track(log):
            e = json.dumps(log)
            Error(error=e).save();
            _hash = hashlib.md5(log['error']).hexdigest()
            u, c = ErrorSummary.objects.get_or_create(key=_hash)
            if c:
                u.error = e
            u.times+=1
            u.last_time = datetime.now()
            u.save();

        @staticmethod
        def count(since=None):
            o = Error.objects
            if since:
                o = o.filter(when__gt=since)
            return o.count()

        @staticmethod
        def latest(items=10, since=None):
            q = ErrorSummary.objects
            if since:
                q = q.filter(last_time__gt=since)
            return q.order_by('-last_time')[:items]

else:
    from models_appengine import *

