import requests
from bs4 import BeautifulSoup


class WebPage:
    def __init__(self, url, site_config):
        self.url = requests.compat.urljoin(site_config['url'], url)
        self.site_config = site_config

        self.request = self._request_page()
        self.html = self._get_html_from_request(self.request)

    def _request_page(self):
        """"Returns request to WebPage url or None"""
        print(f'Requesting {self.url}')
        request = None
        try:
            request = requests.get(self.url)
            if request.status_code != 200:
                request = None
                raise Exception('Status code is not 200')

        except Exception as e:
            print(f'Error while request to {self.url}')
            print(e)
            print('\n')

        return request

    def _get_html_from_request(self, request, parser='lxml'):
        """Returns request text or None"""
        print(f'Parsing html from {self.url}')
        text = None
        try:
            text = BeautifulSoup(request.text, parser)
        except Exception as e:
            print(f'Error while parsing request text from {self.url}')
        return text

    def select(self, selector='body'):
        """Returns content that matches with selector or None"""
        if self.html:
            return self.html.select(selector)
        else:
            return None


class CoursesListPage(WebPage):
    def __init__(self, url, site_config):
        super().__init__(url, site_config=site_config)

    def get_courses_list(self):
        '''Returns links to courses list'''
        course_anchor_list = self.select(self.site_config['queries']['path_courses_links_list'])
        return [course_anchor.get('href') for course_anchor in course_anchor_list]


class CoursePage(WebPage):
    def __init__(self, url, site_config):
        super().__init__(url, site_config)

    def get_reviews_link(self):
        '''Returns link to reviews page'''
        link_to_reviews_a = self.select(self.site_config['queries']['course_link_anchor'])
        if link_to_reviews_a:
            link_to_reviews = link_to_reviews_a[0].get('href')
            return link_to_reviews
        else:
            print('Error')
            print(f'Not found reviews link in {self.url}')

            return None


class ReviewPage(WebPage):
    def __init__(self, url, site_config):
        super().__init__(url, site_config)

    def get_reviews(self):
        self.reviews = self.select(self.site_config['queries']['reviews_list'])

        if self.reviews:
            return [self.get_review_info(review) for review in self.reviews]
        else:
            return []

    def get_review_info(self, review):
        return {
            'user': self.get_user(review),
            'description': self.get_description(review),
            'imageUrl': self.get_image_url(review),
            'stars': self.get_n_stars(review),
        }

    def get_user(self, review):
        return review.select(self.site_config['queries']['review_user'])[0].get_text(strip=True)

    def get_description(self, review):
        return review.select(self.site_config['queries']['review_description'])[0].get_text(strip=True)

    def get_image_url(self, review):
        return review.select(self.site_config['queries']['review_image'])[0].get('src')

    def get_n_stars(self, review):
        return len(review.select(self.site_config['queries']['review_stars_list']))


class ReviewsPages(WebPage):
    def __init__(self, url, site_config):
        super().__init__(url, site_config)

    def get_reviews(self):
        self._update_min_max_paginator()
        reviews = []
        courseName = self.select(self.site_config['queries']['reviews_page_course_name'])
        if courseName:
            courseName = courseName[0].get_text(strip=True)

        for paginator_n in range(self.min_paginator, self.max_paginator + 1):
            actual_review_page = ReviewPage(self.url[:-2] + str(paginator_n), self.site_config)
            reviews.extend(actual_review_page.get_reviews())

        for review in reviews:
            review['course'] = courseName

        return reviews

    def _update_min_max_paginator(self):
        self.min_paginator = 1
        pagination_links = self.select(self.site_config['queries']['pagination_links_list'])
        if pagination_links:
            max_pagination_link = pagination_links[self.site_config['queries']['pagination_max_index']]
            self.max_paginator = int(max_pagination_link.get_text())
        else:
            self.max_paginator = 1
