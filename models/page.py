import ast

import peewee
from peewee import *

from settings.settings import *


class Page(peewee.Model):
    url = peewee.CharField()
    title = peewee.TextField()
    header = peewee.TextField()
    html_errors = peewee.TextField()
    page_meta = peewee.TextField()
    page_links = peewee.TextField()
    starting_url = peewee.CharField()
    yslow_results = peewee.TextField()

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
        starting_url = page_data['starting_url']
        yslow_results = page_data['yslow_results']


        item = Page(url=url,
                    title=title,
                    header=header,
                    html_errors=html_errors,
                    page_meta=page_meta,
                    page_links=page_links,
                    starting_url=starting_url,
                    yslow_results=yslow_results)
        item.save()

    def upsert(self, page_data):
        try:
            # Update existing
            page = Page.get(Page.url==page_data['url'])

            # update value with new value
            page.url = page_data['url']
            page.title = page_data['title']
            page.header = page_data['header']
            page.html_errors = page_data['html_errors']
            page.page_meta = page_data['page_meta']
            page.page_links = page_data['page_links']
            page.starting_url = page_data['starting_url']
            page.yslow_results = page_data['yslow_results']

            page.save()
        except:
            # Create new status entry
            self.add(page_data)


    def count(self):
        return PageItem.select().count()

    def getPages(self):
        pages_list = list()

        for item in Page.select():
            pages_list.append({
                'id': item.id,
                'url':item.url,
                'title': item.title,
                'header': item.header,
                'html_errors': ast.literal_eval(item.html_errors),
                'page_meta': ast.literal_eval(item.page_meta),
                'page_links': ast.literal_eval(item.page_links),
                'starting_url': item.starting_url,
                'yslow_results': item.yslow_results
            })

        return {'pages': pages_list}
