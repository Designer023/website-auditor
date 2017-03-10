import ast

import peewee
from peewee import *

from settings.settings import *


class Visited(peewee.Model):
    url = peewee.CharField()
    session_uuid = peewee.CharField()

    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('url', 'session_uuid' ), True),
        )
try:
    Visited.create_table()
    print 'Page created'
except:
    print 'Page already created'
    pass



class VisitedItem(object):

    def visited_this_session(self, url, session_uuid):
        has_visited = Visited.select(
            Visited.url==url,
            Visited.session_uuid==session_uuid).count()


        if has_visited != 0:
            return True
        return False

    def add(self, url, session_uuid):

        item = Visited(
            url=url,
            session_uuid=session_uuid,
            )
        item.save()

    def upsert(self, url, session_uuid):
        try:
            # Update existing
            _ = Visited.get(Visited.url==url, Visited.session_uuid==session_uuid)
            #if it exists then skip it
        except:
            # Create new status entry
            self.add(url, session_uuid)

    # def count(self):
    #     return Visited.select().count(Visited.session_uuid==session_uuid)
    #
    # def first(self):
    #     data = Visited.select().get(Visited.session_uuid==session_uuid)
    #     return data
    #
    # def popFirst(self):
    #     first = Visited.select().get(Visited.session_uuid==session_uuid)
    #     first.delete_instance()