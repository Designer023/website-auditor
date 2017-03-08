import ast

import peewee
from peewee import *

from settings.settings import *


class Backlog(peewee.Model):
    url = peewee.CharField()
    session_uuid = peewee.CharField()
    starting_url = peewee.CharField()
    depth = peewee.IntegerField()

    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('url', 'session_uuid', 'starting_url' ), True),
        )
try:
    Backlog.create_table()
    print 'Page created'
except:
    print 'Page already created'
    pass



class BacklogItem(object):


    def add(self, url, starting_url, session_uuid, depth):

        item = Backlog(url=url,
                    session_uuid=session_uuid,
                    starting_url=starting_url,
                    depth=depth)
        item.save()

    def upsert(self, url, starting_url, session_uuid, depth):
        try:
            # Update existing
            _ = Backlog.get(Backlog.url==url, Backlog.session_uuid==session_uuid)
            #if it exists then skip it
        except:
            # Create new status entry
            self.add(url, starting_url, session_uuid, depth)

    def count(self):
        return Backlog.select().count()

    def first(self):
        data = Backlog.select().get()
        return data

    def popFirst(self):
        first = Backlog.select().get()
        first.delete_instance()