import ast

import peewee
from peewee import *

from settings.settings import *


class Page(peewee.Model):
    url = peewee.TextField()
    session_uuid = peewee.CharField()
    title = peewee.TextField(null = True)
    header = peewee.TextField()
    html_errors = peewee.TextField(null = True)
    page_meta = peewee.TextField(null = True)
    page_links = peewee.TextField(null = True)
    starting_url = peewee.CharField()
    yslow_results = peewee.TextField(null = True)


    class Meta:
        database = MySQLDatabase(
            database_table,
            user=database_user,
            passwd=database_password
        )
        indexes = (
            (('url', 'session_uuid'), True),
        )
try:
    Page.create_table()
except:
    pass



class PageItem(object):

    def add(self, page_data):

        try:
            yslow_results = page_data['yslow_results']
        except:
            yslow_results = None

        url = page_data['url']
        title = page_data['title']
        header = page_data['header']
        html_errors = page_data['html_errors']
        page_meta = page_data['page_meta']
        page_links = page_data['page_links']
        starting_url = page_data['starting_url']
        session_uuid=page_data['session_uuid']

        try:
            title.decode('utf-8')
            print "string is UTF-8, length %d bytes" % len(title)
        except UnicodeError:
            print "string is not UTF-8"
            title = 'NON UTF-8 Chars. Title not saved!'

        item = Page(url=url,
                    title=title,
                    header=header,
                    html_errors=html_errors,
                    page_meta=page_meta,
                    page_links=page_links,
                    starting_url=starting_url,
                    yslow_results=yslow_results,
                    session_uuid=session_uuid)
        item.save()

    def upsert(self, page_data):
        try:
            # Update existing
            page = Page.get(Page.url==page_data['url'], Page.session_uuid==page_data['session_uuid'])

            try:
                yslow_results = page_data['yslow_results']
            except:
                yslow_results = None


            # update value with new value
            page.url = page_data['url']
            page.title = page_data['title']
            page.header = page_data['header']
            page.html_errors = page_data['html_errors']
            page.page_meta = page_data['page_meta']
            page.page_links = page_data['page_links']
            page.starting_url = page_data['starting_url']
            page.yslow_results = yslow_results
            page.session_uuid = page_data['session_uuid']

            page.save()
        except:
            # Create new status entry
            self.add(page_data)


    def count(self):
        return PageItem.select().count()

    def getPages(self):
        pages_list = list()

        for item in Page.select():

            try:
                page_meta = ast.literal_eval(item.page_meta)
            except:
                page_meta = []

            try:
                yslow_results = ast.literal_eval(item.yslow_results)
            except:
                yslow_results = ''

            try:
                html_errors = ast.literal_eval(item.html_errors)
            except:
                html_errors = []

            pages_list.append({
                'id': item.id,
                'url':item.url,
                'title': item.title,
                'header': item.header,
                'html_errors': html_errors,
                'page_meta': page_meta,
                'page_links': ast.literal_eval(item.page_links),
                'starting_url': item.starting_url,
                'yslow_results': yslow_results,
                'session_uuid': item.session_uuid
            })

        return {'pages': pages_list}


    def getPagesForSession(self, session_uuid):
        pages_list = list()

        for item in Page.filter(session_uuid=session_uuid):

            try:
                page_meta = ast.literal_eval(item.page_meta)
            except:
                page_meta = []

            try:
                yslow_results = ast.literal_eval(item.yslow_results)
            except:
                yslow_results = ''

            try:
                html_errors = ast.literal_eval(item.html_errors)
            except:
                html_errors = []

            pages_list.append({
                'id': item.id,
                'url':item.url,
                'title': item.title,
                'header': item.header,
                'html_errors': html_errors,
                'page_meta': page_meta,
                'page_links': ast.literal_eval(item.page_links),
                'starting_url': item.starting_url,
                'yslow_results': yslow_results,
                'session_uuid': item.session_uuid
            })

        return {'pages': pages_list}

    def update_yslow(self, url, yslow_results):
        try:
            page = Page.get(Page.url == url)
            page.yslow_results = yslow_results
            page.save()
        except:
            pass



    def get_page_data(self, id):
        try:

            page = Page.get(Page.id == id)

            page_data = {}


            try:
                page_meta = ast.literal_eval(page.page_meta)
            except:
                page_meta = []

            try:
                yslow_results = ast.literal_eval(page.yslow_results)
            except:
                yslow_results = ''

            try:
                html_errors = ast.literal_eval(page.html_errors)
            except:
                html_errors = []

            page_data['url'] = page.url
            page_data['starting_url'] = page.starting_url
            page_data['header'] = page.header
            page_data['title'] = page.title
            page_data['html_errors'] = html_errors
            page_data['page_meta'] = page_meta
            page_data['page_links'] = ast.literal_eval(page.page_links)
            page_data['yslow_results'] = yslow_results
            page_data['session_uuid'] = page.session_uuid

            return page_data

        except:
            return "No Page found"




