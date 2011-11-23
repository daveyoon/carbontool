
# GOOGLE STUFF
from google.appengine.ext import db

class Work(db.Model):
    """ key value to store json models """
    json = db.TextProperty(default='[]')
    
    def unique_id(self):
        return self.key().id()
    

class Error(db.Model):
    """ simple class to store application errors """
    error = db.TextProperty(default='')
    when = db.DateTimeProperty(auto_now=True) 

    @staticmethod
    def track(log):
        Error(error=log).put();

    @staticmethod
    def latest(items=10, since=None):
        q = Error.all().
        if since:
            q = q.filter('when >', since) 
        return q.order('-when').fetch(items)
