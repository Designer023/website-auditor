import peewee
import time
from peewee import *

from settings.settings import *

STATUS_CHOICES = (
    (0, 'Initialised'),
    (1, 'Incomplete'),
    (2, 'Complete'),
    (3, 'Archived')
)

class Session(peewee.Model):
    starting_url = peewee.CharField()
    session_uuid = peewee.CharField()
    pages = peewee.IntegerField(default=0)
    queued = peewee.IntegerField(default=0)
    status_code = peewee.IntegerField(default=0)
    timestamp = peewee.TimestampField()

    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('starting_url', 'session_uuid'), True),
        )
try:
    Session.create_table()
except:
    pass


class SessionItem(object):

    def add(self, starting_url, session_uuid):

        ts = time.time()

        session = Session(
            starting_url=starting_url,
            session_uuid=session_uuid,
            pages=0,
            queued=0,
            status=0,
            timestamp=ts
            )
        session.save()

    def create(self, starting_url, session_uuid):
        try:
            # Update existing
            _ = Session.get(
                Session.starting_url==starting_url,
                Session.session_uuid==session_uuid
            )
            # If it exists then skip it
        except:
            # Create new status entry
            self.add(starting_url, session_uuid)

    def update_stats(self, starting_url, session_uuid, queue_count, page_count, status_code):
        session = Session.get(
            Session.starting_url == starting_url,
            Session.session_uuid == session_uuid
        )

        session.queued = queue_count
        session.pages = page_count
        session.status_code = status_code

        session.save()


    def update_queue(self, starting_url, session_uuid, count):
        session = Session.get(
            Session.starting_url==starting_url,
            Session.session_uuid==session_uuid
        )

        session.queued = count

        session.save()

    def update_status_code(self, starting_url, session_uuid, status_code):
        session = Session.get(
            Session.starting_url==starting_url,
            Session.session_uuid==session_uuid
        )

        session.status_code = status_code

        session.save()

    def update_pages(self, starting_url, session_uuid, count):
        session = Session.get(
            Session.starting_url == starting_url,
            Session.session_uuid == session_uuid
        )

        session.pages = count

        session.save()

    def session_progress(self, starting_url, session_uuid):
        session = Session.get(Session.starting_url == starting_url,
                              Session.session_uuid == session_uuid)

        pages = session.pages
        queued = session.queued
        progress = {}
        progress['percent'] = 100 / float(pages + queued) * float(pages)
        progress['page_count'] = pages
        progress['queue_count'] = queued

        return progress


    def get_sessions(self, session_uuid=None):

        if session_uuid is not None:
            session_objects = Session.filter(
                Session.session_uuid==session_uuid
            )
        else:
            session_objects = Session.select()\
                .order_by(Session.timestamp.desc())

        sessions = list()

        for item in session_objects:
            status_dict = dict(STATUS_CHOICES)
            session = {}
            session['id'] = item.id
            session['uuid'] = item.session_uuid
            session['url'] = item.starting_url
            session['pages'] = item.pages
            session['queue'] = item.queued
            session['status'] = status_dict[item.status_code]
            session['status_code'] = item.status_code
            session['timestamp'] = item.timestamp

            total_items = item.pages + item.queued
            try:
                percent = 100 / float(total_items) * float(item.pages)
                session['percent'] = round(percent, 2)
            except ZeroDivisionError:
                session['percent'] = 0

            sessions.append(session)

        return sessions
