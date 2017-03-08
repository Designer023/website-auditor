import ast

import peewee
from peewee import *

from settings.settings import *


class Backlog(peewee.Model):
    url = peewee.CharField()
    session_uuid = peewee.CharField()
    starting_url = peewee.CharField()

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

    def __init__(self):
        print "Backlog initiated"

    # def add(self, url, starting_url, session_uuid):
    #
    #     # item = Page(url=url,
    #     #             session_uuid=session_uuid,
    #     #             starting_url=starting_url)
    #     # item.save()
    #
    # def upsert(self, url, starting_url, session_uuid):
    #     # try:
    #     #     # Update existing
    #     #     page = Page.get(Page.url==page_data['url'])
    #     #
    #     #     # update value with new value
    #     #     page.url = page_data['url']
    #     #     page.title = page_data['title']
    #     #     page.header = page_data['header']
    #     #     page.html_errors = page_data['html_errors']
    #     #     page.page_meta = page_data['page_meta']
    #     #     page.page_links = page_data['page_links']
    #     #     page.starting_url = page_data['starting_url']
    #     #
    #     #     page.save()
    #     # except:
    #     #     # Create new status entry
    #     #     self.add(page_data, starting_url)
    #
    #
    # def count(self):
    #     # return QueuedItem.select().count()
    #
    # def getPages(self):
    #     # pages_list = list()
    #     #
    #     # for item in Page.select():
    #     #     pages_list.append({
    #     #         'id': item.id,
    #     #         'url':item.url,
    #     #         'title': item.title,
    #     #         'header': item.header,
    #     #         'html_errors': ast.literal_eval(item.html_errors),
    #     #         'page_meta': ast.literal_eval(item.page_meta),
    #     #         'page_links': ast.literal_eval(item.page_links),
    #     #         'starting_url': item.starting_url
    #     #     })
    #     #
    #     # return {'pages': pages_list}