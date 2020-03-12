from common import get_config
from models import CoursesListPage, CoursePage
import re

course_page_link_re = re.compile(r'/clases/([\w-]*)/?$')

if __name__ == "__main__":
    config = get_config()
    for site_config in config['courses_sites'].values():
        for course_page_url in site_config['paths']:
            actual_courses_list_page = CoursesListPage(site_config['url'] + course_page_url, site_config)
            for course_link_raw in actual_courses_list_page.get_courses_list():
                course_link = '/cursos/' + course_page_link_re.match(course_link_raw)[1]
                actual_course_page = CoursePage(course_link, site_config)
