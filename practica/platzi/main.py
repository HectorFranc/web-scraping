from common import get_config
from models import CoursesListPage

if __name__ == "__main__":
    config = get_config()
    for site_config in config['courses_sites'].values():
        for course_page_url in site_config['paths']:
            actual_courses_list_page = CoursesListPage(site_config['url'] + course_page_url, site_config)
            print(actual_courses_list_page.get_courses_list())
