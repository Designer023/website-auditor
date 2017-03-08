import peewee
from peewee import *

from settings.settings import *


class Page(peewee.Model):
    url = peewee.CharField()
    title = peewee.CharField()
    header = peewee.TextField()
    html_errors = peewee.TextField()
    page_meta = peewee.TextField()
    page_links = peewee.TextField()

    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('url'), True),
        )
try:
    Page.create_table()
    print 'Page created'
except:
    print 'Page already created'
    pass



class PageItem(object):

    def __init__(self):
        print "PageItem initiated"

    def add(self, page_data):
        url = page_data['url']
        title = page_data['title']
        header = page_data['header']
        html_errors = page_data['html_errors']
        page_meta = page_data['page_meta']
        page_links = page_data['page_links']

        item = Page(url=url,
                    title=title,
                    header=header,
                    html_errors=html_errors,
                    page_meta=page_meta,
                    page_links=page_links)
        item.save()

    def count(self):
        return QueuedItem.select().count()


        return queue_list