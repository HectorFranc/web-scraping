from common import get_config
from models import CoursesListPage, CoursePage, ReviewsPages
import re
import pandas as pd

course_page_link_re = re.compile(r'/clases/([\w-]*)/?$')

if __name__ == "__main__":
    config = get_config()
    for site_config in config['courses_sites'].values():
        for course_page_url in site_config['paths']:
            actual_courses_list_page = CoursesListPage(site_config['url'] + course_page_url, site_config)

            reviews = []
            for course_link_raw in actual_courses_list_page.get_courses_list():
                course_link = course_link_raw  # '/cursos/' + course_page_link_re.match(course_link_raw)[1]
                actual_course_page = CoursePage(course_link, site_config)

                actual_course_review_page = ReviewsPages(actual_course_page.get_reviews_link(), site_config)
                reviews.extend(actual_course_review_page.get_reviews())
            df = pd.DataFrame(reviews)
            df.to_csv('data.csv')
