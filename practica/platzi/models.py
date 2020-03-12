import requests
from bs4 import BeautifulSoup


class WebPage:
    def __init__(self, url, site_config):
        self.url = url
        self.site_config = site_config

        self.request = self._request_page()
        self.html = self._get_html_from_request(self.request)

    def _request_page(self):
        """"Returns request to WebPage url or None"""
        print(f'Requesting {self.url}')
        try:
            request = requests.get(self.url)
            if request.status_code != 200:
                request = None
                raise Exception('Status code is not 200')

        except Exception as e:
            print(f'Error while request to {self.url}')
            print(e)
            print('\n')

        return request or None

    def _get_html_from_request(self, request, parser='lxml'):
        """Returns request text or None"""
        print(f'Parsing html from {self.url}')
        try:
            text = BeautifulSoup(request.text, parser)
        except Exception as e:
            print(f'Error while parsing request text from {self.url}')
        return text or None

    def select(self, selector='body'):
        """Returns content that matches with selector or None"""
        return self.html.select(selector)


class CoursesListPage(WebPage):
    def __init__(self, url, site_config):
        super().__init__(url, site_config=site_config)

    def get_courses_list(self):
        '''Returns courses (html elements list)'''
        course_anchor_list = self.select(self.site_config['queries']['path_courses_links_list'])
        return [course_anchor.get('href') for course_anchor in course_anchor_list]
