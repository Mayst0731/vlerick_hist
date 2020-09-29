'''
This file is to get course url and course name with category name and category url
'''
from scrapingfiles.parse_pages import *
from urllib import parse


def get_all_courses_url(category_page_obj,category_url,category_name):
    lst = []
    course_elements = category_page_obj.find_all('div',attrs={'class':'programItem clearfix grid_12 alpha'})
    course_elements += category_page_obj.find_all('div',attrs={'class':'programItem clearfix grid_12 omega'})
    length = len(course_elements)
    print(f'length of courses {length}')
    for course_element in course_elements:
        course = {}
        course_name = course_element.find('h2').text
        course_url_post = course_element.find('h2').a.get('href')
        course_url = parse.urljoin(category_url, course_url_post)
        course["name"] = course_name
        course['url'] = course_url
        course['category_name'] = category_name
        course['category_url'] = category_url
        lst.append(course)
    return lst

# cateogry_obj = parse_page_to_obj('https://www.vlerick.com/en/programmes/management-programmes/accounting-finance')
# category_url = 'https://www.vlerick.com/en/programmes/management-programmes/accounting-finance'
# print(get_all_courses_url(cateogry_obj,category_url,category_name))
