from urllib import parse
from scrapingfiles.parse_pages import parse_page_to_obj
from urllib import parse

from scrapingfiles.read_write import write_course_list_to_json

'''
Mission 1: Get all faculty info for storing into a single file

{name:'',
title:'',
pic_url:'',
university_school:'',
intro_desc:'',
pdf_url:''
}


Mission 2: Get only name and title and store into each course info 
{
name : '',
title :''
}

'''

# get the link of faculties from course page
def get_faculty_url(course_url,course_obj):
    faculty_url = ''
    a_link = course_obj.find('a',text='Faculty')
    if a_link:
        faculty_url_post = a_link.get('href')
        faculty_url = parse.urljoin(course_url,faculty_url_post)
    return faculty_url


# Get all the information of faculties
def get_faculty_info(faculty_obj):
    tables = faculty_obj.find_all('table')
    faculties = []
    for table in tables:
        person = {}
        tds = table.tbody.tr.find_all('td')

        img = ''
        try:
            img = tds[0].img.get('src')
        except Exception:
            pass

        name = ""
        try:
            name_obj = tds[1].a
            # check if name obj exists
            if not name_obj:
                name_obj = tds[1].p

            name = name_obj.text
        except Exception:
            pass


        title = ''
            # check if title span exists
        try:
            title = tds[1].span.text
        except Exception:
            print(f'{name} has no title')

        intro = ''
        try:
            intro = str(tds[1].p.next_sibling)
        except Exception:
            print(f'{name} has no intro')

        if img.startswith('/~/'):
            img=complete_img_url(img)

        # cut off useless info in name
        name = delete_titles_in_name(name)
        name = cut_title_from_name(name)
        if len(name) != 0:
            person['name'] = name
            person['title'] = title.strip()
            person['pic_url'] = img
            person['intro_desc'] = intro.strip()
            person['university_school'] = '2222_EUR'
            person['pdf_url'] = ''
            faculties.append(person)
    return faculties


#Get partial info of each faculty for storing to the course detail
def get_partial_faculty_info(faculty_url,faculty_obj):
    '''
    :param faculty_url,faculty_obj
    :return: partial faculty info list
    '''
    tables = faculty_obj.find_all('table')
    faculties = []
    for table in tables:
        person = {}
        tds = table.tbody.tr.find_all('td')
        name = tds[1].a.text
        name = delete_titles_in_name(name)
        name = cut_title_from_name(name)
        title = tds[1].span.text.strip()
        person['name'] = name
        person['title'] = title
        faculties.append(person)
    return faculties


def delete_titles_in_name(name):
    '''
    The function is for clearing the useless information
    '''
    name_lst = name.split()
    if "Prof" in name_lst:
        print(f'name_lst before: {name_lst}')
        name_lst.remove("Prof")
        print(f'name_lst after: {name_lst}')
    if "Prof." in name_lst:
        print(f'name_lst before: {name_lst}')
        name_lst.remove("Prof.")
        print(f'name_lst after: {name_lst}')
    if "Professor" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Professor = name_lst.index("Professor")
        name_lst = name_lst[:index_of_Professor]
        print(f'name_lst after: {name_lst}')
    if "CEO" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_CEO = name_lst.index("CEO")
        name_lst = name_lst[:index_of_CEO]
        print(f'name_lst after: {name_lst}')
    if "Founding" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Founding = name_lst.index("Founding")
        name_lst = name_lst[:index_of_Founding]
        print(f'name_lst after: {name_lst}')
    if "Managing" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Managing = name_lst.index("Managing")
        name_lst = name_lst[:index_of_Managing]
        print(f'name_lst after: {name_lst}')
    if "Director" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Director = name_lst.index("Director")
        name_lst = name_lst[:index_of_Director]
        print(f'name_lst after: {name_lst}')
    if "dr." in name_lst:
        print(f'name_lst before: {name_lst}')
        name_lst.remove("dr.")
        print(f'name_lst after: {name_lst}')
    if "Lecturer" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Lecturer = name_lst.index("Lecturer")
        name_lst = name_lst[:index_of_Lecturer]
        print(f'name_lst after: {name_lst}')
    if "Executive" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Executive = name_lst.index("Executive")
        name_lst = name_lst[:index_of_Executive]
        print(f'name_lst after: {name_lst}')
    if "Chief" in name_lst:
        print(f'name_lst before: {name_lst}')
        index_of_Chief = name_lst.index("Chief")
        name_lst = name_lst[:index_of_Chief]
        print(f'name_lst after: {name_lst}')
    if len(name_lst) > 10:
        name_lst = [""]
    new_name = " ".join(name_lst)
    return new_name


def cut_title_from_name(name):
    new_name = name
    if '\n' in name:
        name_lst = name.split('\n')
        new_name = name_lst[0]
    return new_name


def complete_img_url(src):
    url = parse.urljoin("https://www.vlerick.com", src)
    return url







