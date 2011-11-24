# -*- encoding: utf-8 -*-

"""
this module contains views that serve the REST-like API 
for client-side backbone application
"""

import logging
import urllib2
import time
try:
    import json
except:
    import simplejson as json

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from baseconv import base62
from models import Work, Error


BASE_ID = 123456
@csrf_exempt
def work(request, work_hash=None):

    status = 200
    work = None
    if work_hash:
        id = base62.to_decimal(work_hash)
        work = Work.get_by_id(id - BASE_ID)
        if not work:
            raise Http404

    # create work
    if request.method == "POST":
        w = Work()
        w.put();
        data = json.dumps({'id': base62.from_decimal(BASE_ID + w.unique_id())})

    # update
    elif request.method == "PUT":
        if work:
            work.json = request.raw_post_data
            work.put()
            data = request.raw_post_data
        pass
    # remove
    elif request.method == "DELETE":
        work.delete();
        status = 204
        data = ''
        pass
    # get
    else:
        if not work:
          data = '{"error": "does not exist"}'
          status = 404
        else: 
          data = work.json
        pass

    return HttpResponse(data, status=status, mimetype='application/json')

@csrf_exempt
def proxy(request, host):
    if request.method == "POST":
        f = urllib2.urlopen(host, request.raw_post_data)
        nfo = f.info()
        r = HttpResponse(f.read())
        for h in nfo:
          if h in ['content-type']:
            r[h] = nfo.getheader(h)
        return r
    return HttpResponse("use POST", status=404)

def error_track(request):
    err = request.GET.get('e', '')
    ua = request.META['HTTP_USER_AGENT']
    host = request.get_host()
    if err:
        Error.track({
            'error': err,
            'ua': ua,
            'host': host
        })
    return HttpResponse('', mimetype='application/json')

@csrf_exempt
def error(request):
    if request.method == "POST":
        Error.track(request.raw_post_data)
        return HttpResponse("logged, thanks!")
    else:
        data = {
            'count': Error.count(),
            'latest': [x.to_dict() for x in Error.latest()]
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')

def errors(request):
    text = '\n'.join([x.when.isoformat() + " =>" + x.error for x in Error.latest()])
    return HttpResponse(text, mimetype='text/plain')



