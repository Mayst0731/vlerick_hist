from urllib.parse import urljoin
import re
from scrapingfiles.parse_pages import parse_page_to_obj
import requests
from bs4 import BeautifulSoup


def practical_page_link(course_obj):
    '''
    :param course_obj
    :return: practical info page link
    '''
    try:
        practical_a_tag = course_obj.find('a', text=re.compile("Practical"))
        practical_info_link = urljoin("https://www.vlerick.com", practical_a_tag.get('href'))
    except:
        practical_info_link = ''
    return practical_info_link


def location_for_one_version_course(practical_info_page_obj):
    '''
    :param practical_info_page_obj: -> Object
    :return: location: -> String
    '''
    location = ''
    try:
        loc_session = practical_info_page_obj.find('p', attrs={'id': 'corporatebody_0_phLocations'})
        loc_session_title = loc_session.strong.extract()
        location = loc_session.text.strip()
    except:
        pass
    return location


def fee_in_pratical_page(practical_info_page_obj):
    '''
    :param practical_info_page_obj: -> Object
    :return: tuition related information -> Object
    '''
    obj = {'tuition': '',
           'currency': '',
           'tuition_desc': ''}
    try:
        print(f'get into try=============')
        fee_session = practical_info_page_obj.find('p', attrs={'id': 'corporatebody_0_phFees'})
        fee_session_text_list = fee_session.text.split()
        tuition = fee_session_text_list[1]
        currency = fee_session_text_list[2]
        tuition_desc = ' '.join(fee_session_text_list[3:])
        obj['tuition'] = tuition
        obj['currency'] = currency
        obj['tuition_desc'] = tuition_desc
    except Exception as e:
        print(e)
    return obj



def course_version_info(course_obj, practical_info_page_obj):
    '''
    :param course_obj
    :return:
    '''
    versions = 1
    locations = set()
    versions_info_lst = list()
    try:
        fee_related_info = fee_in_pratical_page(practical_info_page_obj)
        ver_outside_obj = course_obj.find('div', attrs={"class": "editionsWrapper"})
        ver_objs = ver_outside_obj.find_all('div')
        length = length_for_multiple_version_course(practical_info_page_obj)
        for obj in ver_objs:
            version_obj = {}
            location_link = obj.find('a')
            location = location_link.text
            if '...' in location:
                versions = 10
                break
            if location not in locations:
                locations.add(location)
                effective_start_date_session = obj.find_all('p')[0]
                effective_start_date_title = effective_start_date_session.strong.extract()
                effective_start_date = effective_start_date_session.text.strip('\n')
                language_session = obj.find_all('p')[2]
                language_title = language_session.strong.extract()
                language = language_session.text.strip('\n')
                version_obj['location'] = location
                version_obj['effective_start_date'] = effective_start_date
                version_obj['language'] = language

                version_obj.update(fee_related_info)
                version_obj['length'] = length
                versions_info_lst.append(version_obj)
    except:
        pass
    if len(locations) != 0:
        versions = len(locations)
    try:
        for version_obj in versions_info_lst:
            version_obj['versions'] = versions
    except:
        pass
    print(f'versions is {versions}')
    if versions == 1:
        version_obj = {}
        info_session = course_obj.find('div', attrs={'class': 'programDetails'})
        length_session = info_session.find_all('p')[1]
        length_title = length_session.strong.extract()
        length = length_session.text
        effective_start_date_session = info_session.find_all('p')[2]
        effective_start_date_title = effective_start_date_session.strong.extract()
        effective_start_date = effective_start_date_session.text
        language_session = info_session.find_all('p')[3]
        language_title = language_session.strong.extract()
        language = language_session.text
        version_obj['length'] = length.strip('\n')
        version_obj['effective_start_date'] = effective_start_date.strip('\n')
        version_obj['language'] = language.strip('\n')
        version_obj['versions'] = versions
        version_obj['location'] = location_for_one_version_course(practical_info_page_obj)

        fee_related_info = fee_in_pratical_page(practical_info_page_obj)
        print(f'1 version fee: {fee_related_info}')
        version_obj.update(fee_related_info)

        versions_info_lst.append(version_obj)
    return versions_info_lst


def length_for_multiple_version_course(practical_info_page_obj):
    length = ''
    try:

        length_session = practical_info_page_obj.find('p', attrs={'id': 'corporatebody_0_phLength'})
        length_session_title = length_session.strong.extract()
        length = length_session.text.strip()

    except:
        pass
    return length




