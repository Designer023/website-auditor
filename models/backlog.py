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
except:
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

    def count_session(self, session_uuid):
        return Backlog.select().count(Backlog.session_uuid==session_uuid)

    def first_session(self, session_uuid):
        # data = Backlog.select().select(Backlog.session_uuid==session_uuid)
        data = Backlog.select().get()
        return data

    def pop_first_session(self, session_uuid):
        # first = Backlog.select().select(Backlog.session_uuid==session_uuid)
        first = Backlog.select().get()
        first.delete_instance()