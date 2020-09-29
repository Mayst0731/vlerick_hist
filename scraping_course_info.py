import re
from urllib.parse import urljoin

from scrapingfiles.parse_pages import parse_page_to_obj

'''
test cases
'''

COURSE_URL_LIST = ['https://www.vlerick.com/en/programmes/management-programmes/accounting-finance/financial-management-for-nonfinancial-managers',
'https://www.vlerick.com/en/programmes/management-programmes/accounting-finance/understanding-annual-reports']


def test_res(course_url_list,fn):
    for url in course_url_list:
        course_obj = parse_page_to_obj(url)
        res = fn(course_obj)
        print(res)

'''
Get course info
'''


def get_course_name(course_obj):
    span_obj = course_obj.find("div",attrs={"class":"breadcrumb grid_24 alpha omega"}).find("span")
    course_name = span_obj.text
    return course_name


def get_course_url():
    pass


def get_category_name(course_obj):
    course_name_obj = course_obj.find("div",attrs={"class":"breadcrumb grid_24 alpha omega"}).find("span")
    cate_obj_post = course_name_obj.find_previous_sibling('a')
    cate_obj_pre = cate_obj_post.find_previous_sibling('a')
    cate_pre = cate_obj_pre.text
    cate_post = cate_obj_post.text
    cate_name = f"{cate_pre}-{cate_post}"
    return cate_name


def get_course_type():
    type = 'Onsite'
    return type


def get_course_version(course_obj):
    '''
    :param course_obj:
    :return: tuple (course_version_number, version_related_page_link)
    '''
    ver_outside_obj = course_obj.find('div',attrs={"class":"editionsWrapper"})
    ver_objs = ver_outside_obj.find_all('div')
    link = ''
    locations = set()
    for obj in ver_objs:
        try:
            location_link = obj.find('a')
            location = location_link.text
            if location not in locations:
                locations.add(location)
            if len(link) == 0:
                link = urljoin("https://www.vlerick.com",location_link.get('href'))
        except:
            continue
    return (len(locations),link)
url = 'https://www.vlerick.com/en/programmes/management-programmes/accounting-finance/financial-management-for-nonfinancial-managers'
obj = parse_page_to_obj(url)
print(get_course_version(obj))


def get_ver_related_info(practical_info_page):
    '''
    :param practical_info_page:
    :return: list of objects [{location,start_date,fee}]
    '''
    loc_set = set()
    info_sessions = practical_info_page.find_all('div',attrs={'class':'box-wheading no-border small-margin'})
    info_objs = []
    for each_session in info_sessions:
         info_objs += each_session.find_all('div')

    for info_obj in info_objs:
        loc = info_obj.find('strong',text='Venue(s):').parent.a.text
        if loc not in loc_set:
            loc_set.add(loc)
            length= info_obj.find('strong',text='Length:').parent.text.replace(u'Length:',u'').strip()
            dates = info_obj.find('strong', text='Date(s):').parent.text.replace(u'Date(s):',u'').strip()
            language = info_obj.find('strong', text='Language:').parent.text.replace(u'Language:',u'').strip()
            fee = info_obj.find('strong', text='Fee:').parent.text.replace(u'Fee:',u'').strip()
            print('=========================================================================================')
            print(f'location: {loc} length: {length} dates: {dates} language: {language} fee: {fee}')
    pass

# url = "https://www.vlerick.com/en/programmes/management-programmes/accounting-finance/financial-management-for-nonfinancial-managers/practical-info#financieel-management-voor-de-niet-financile-manager-voorjaar-i-2021"
# obj = parse_page_to_obj(url)
# get_ver_related_info(obj)


def get_course_location_ver():
    pass


def get_course_currency_ver():
    pass


def get_course_tuition_ver():
    pass


def get_course_duration_num_ver():
    pass


def get_course_duration_type_ver():
    pass


def get_course_duration_consecutive_ver():
    pass


def get_course_language_ver():
    pass


def get_course_duration_desc_ver():
    pass


def get_course_start_date_ver():
    pass


def get_course_desc(course_obj):
    desc_session_div = course_obj.find('div',attrs={'class':'rte'})
    children_objs = desc_session_div.findChildren()
    para = ''
    for child in children_objs:
        if child.name == 'hr':
            break
        elif child.name == 'p':
            para += '\n' + child.text
    return para



def get_course_testimonials_other_link(testimonial_page_obj):

    testis = testimonial_page_obj.find_all('tr')
    print(testis)
    testi_list = []
    for testi_obj in testis:
        name = ''
        title = ''
        company = ''
        testimonial_statement = ''
        picture_url = ''
        visual_url = ''
        testi = {}
        try:
            name = testi_obj.find_all('td')[1].p.strong.text
        except Exception as e:
            print(e)
        try:
            title = testi_obj.find_all('td')[1].p.span.text
        except Exception as e:
            print(e)
        try:
            extract_name_obj = testi_obj.find_all('td')[1].p.strong.extract()
            extract_title_obj = testi_obj.find_all('td')[1].p.span.extract()
            company = testi_obj.find_all('td')[1].p.text
        except Exception as e:
            print(f'company: {e}')

        try:
            picture_url = testi_obj.find_all('td')[0].img.get('src')
        except Exception as e:
            print(f'picture_url: {e}')

        try:
            testimonial_statement = testi_obj.find_all('td')[1].em.text
        except Exception as e:
            print(f'testimonial_statement: {e}')

        if len(name) == 0:
            name_obj = testi_obj.find_all('p')[0].strong
            name = name_obj.text

            title_obj = testi_obj.find_all('p')[0].span
            title = title_obj.text

            extract_name_obj = testi_obj.find_all('p')[0].strong.extract()
            extract_title_obj = testi_obj.find_all('p')[0].span.extract()
            company = testi_obj.find_all('p')[0].text

            visual_url = testi_obj.iframe.get('src')


        testi['name'] = name
        testi['title'] = title
        company = re.sub(r'[^\w\s]', '', company)
        testi['company'] = company.strip()
        testi['picture_url'] = picture_url
        testi['visual_url'] = visual_url
        testi['testimonial_statement'] = testimonial_statement.replace(u'\xa0', u' ')
        testi_list.append(testi)
    return testi_list


def get_course_who_should_attend_other_link(who_should_attend_obj):
    who_should_attend_div = who_should_attend_obj.find('div', attrs={'class': 'rte'})
    children_objs = who_should_attend_div.findChildren()
    who_should_attend = ''
    for child in children_objs:
        if child.name == 'p':
            who_should_attend += '\n' + child.text
    return who_should_attend


def get_course_take_away_other_link(take_away_page_obj):
    take_away_session_div = take_away_page_obj.find('div', attrs={'class': 'rte'})
    children_objs = take_away_session_div.findChildren()
    take_away = ''
    for child in children_objs:
        if child.name == 'p':
            take_away += '\n'+ child.text
    return take_away





def integrate_all_info():
    university_schools = '3399_EUR'
    active = True
    priority = "Non-sponsor"
    publish = 'public'

    pass







