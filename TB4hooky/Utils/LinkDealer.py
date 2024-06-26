from html.parser import HTMLParser
import requests


class LinksDealer(object):

    @staticmethod
    def _get_links(addr):
        links = set()

        class LinksParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    attrs = dict(attrs)
                    links.add(attrs.get('href').rstrip('/'))


        try:
            resp = requests.get(addr)
            content = resp.text
            parser = LinksParser()
            parser.feed(content)
        except Exception as _:
            pass
        return links

    @staticmethod
    def get_link(addr):
        return LinksDealer._get_links(addr)

    @staticmethod
    def _filter_links(links):
        return links.startswith(("http://", "https://"))

    @staticmethod
    def filter_links(links):
        return LinksDealer._filter_links(links)

    @staticmethod
    def _get_filehandle_links(addr):
        links = set()

        class LinksParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    attrs = dict(attrs)
                    links.add(attrs.get('href'))

        try:
            resp = requests.get(addr)
            content = resp.text
            parser = LinksParser()
            parser.feed(content)
        except Exception as _:
            pass
        return links

    @staticmethod
    def get_filehandle_links(addr):
        return LinksDealer._get_filehandle_links(addr)