import peewee
from peewee import *

from settings.settings import *


class Session(peewee.Model):
    starting_url = peewee.CharField()
    session_uuid = peewee.CharField()
    pages = peewee.IntegerField()
    queued = peewee.IntegerField()



    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('starting_url', 'session_uuid' ), True),
        )
try:
    Session.create_table()
except:
    pass


class SessionItem(object):

    def add(self, starting_url, session_uuid):

        session = Session(
            starting_url=starting_url,
            session_uuid=session_uuid,
            pages=0,
            queued=0
            )
        session.save()

    def create(self, starting_url, session_uuid):
        try:
            # Update existing
            _ = Session.get(Session.starting_url==starting_url, Session.session_uuid==session_uuid)
            #if it exists then skip it
        except:
            # Create new status entry
            self.add(starting_url, session_uuid)

    def update_queue(self, starting_url, session_uuid, count):
        session = Session.get(Session.starting_url == starting_url,
                        Session.session_uuid == session_uuid)

        session.queued = count

        session.save()

    def update_pages(self, starting_url, session_uuid, count):
        session = Session.get(Session.starting_url == starting_url,
                        Session.session_uuid == session_uuid)

        session.pages = count

        session.save()

    def session_progress(self, starting_url, session_uuid):
        session = Session.get(Session.starting_url == starting_url,
                              Session.session_uuid == session_uuid)

        pages = session.pages
        queued = session.queued
        progress = {}
        progress['percent'] = 100 / (pages + queued) * pages
        progress['page_count'] = pages
        progress['queue_count'] = queued

        return progress


    def get_sessions(self, session_uuid = None):

        if session_uuid is not None:
            session_objects = Session.filter(Session.session_uuid == session_uuid)
        else:
            session_objects = Session.select()

        sessions = list()

        for item in session_objects:
            session = {}
            session['uuid'] = item.session_uuid
            session['url'] = item.starting_url
            session['pages'] = item.pages
            session['queue'] = item.queued
            try:
                percent = 100 / (item.pages + item.queued) * item.pages
                session['percent'] = percent
            except ZeroDivisionError:
                session['percent'] = 0

            sessions.append(session)

        return sessions
