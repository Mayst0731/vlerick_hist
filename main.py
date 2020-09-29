from scrapingfiles.parse_pages import parse_page_to_obj
from scrapingfiles.read_write import write_category_list_to_csv, write_category_list_to_json, write_course_list_to_json
from scrapingfiles.scraping_category_list import get_all_categories
# from scrapingfiles.scraping_course_list import  get_all_courses_url
# from scrapingfiles.scraping_faculties import get_faculty_url, get_faculty_info
from scrapingfiles.scraping_course_list import get_all_courses_url
from scrapingfiles.scraping_faculties import get_faculty_url, get_faculty_info

START_URL = "https://www.vlerick.com/en/programmes/management-programmes"


# Get obj of each category page
def get_category_page_dict(**kwargs):
    dict = {}
    for category_name, category_url in kwargs.items():
        try:
            dict[category_name] = parse_page_to_obj(category_url)
        except Exception as e:
            print(f'{category_url} has problem: \n{e}')
        finally:
            print(f'{category_name} is parsed successfully!')
    return dict


def get_all_category_info(**kwargs):
    cate_lst = []
    for category_name,category_url in kwargs.items():
        cate_obj = {}
        cate_obj['category'] = category_name
        cate_obj['url'] = category_url
        cate_obj['parent_url'] = START_URL
        cate_lst.append(cate_obj)
    return cate_lst



def main():
    '''
    get category list
    '''

    # {category_name:category_url,....}
    category_url_map = get_all_categories(START_URL)

    # [{name:***, url: ***, parent_url:***},...]
    category_list_info = get_all_category_info(**category_url_map)
    print(f'category_list_info:\n{category_list_info}')
    write_category_list_to_json(category_list_info, '../outputfiles/CATEGORY_3399_EUR_0910.json')

    '''
    get course list
    '''
    # {category_name: category_page_obj,...}
    category_page_map = get_category_page_dict(**category_url_map)

    category_name_url_obj_collections = []
    for cate_name,cate_url in category_url_map.items():
        cate = {}
        cate['cate_name'] = cate_name
        cate['cate_url'] = cate_url
        cate['obj'] = category_page_map[cate_name]
        category_name_url_obj_collections.append(cate)

    course_list = []
    for cate in category_name_url_obj_collections:
        course_list += get_all_courses_url(cate['obj'], cate['cate_url'], cate['cate_name'])
    write_category_list_to_json(course_list, '../outputfiles/COURSE_LIST_3399_EUR_0910.json')


    '''
    get faculty list    
    '''
    course_name_url_obj_collections = []

    # get all courses' page_obj
    for course in course_list:
        _course = {}
        _course['course_name'] = course['name']
        _course['course_url'] = course['url']
        _course['obj'] = parse_page_to_obj(course['url'])
        print(f"{_course['course_name']} has been parsed")
        course_name_url_obj_collections.append(_course)

    # get faculty link in each course and add faculty_url into collections
    for course in course_name_url_obj_collections:
        course['faculty_url'] = get_faculty_url(course['course_url'],course['obj'])
        print(f"successfully get {course['course_name']} faculty url")
    #  parse faculty url to get faculty obj and add page objs into the collections
    for course in course_name_url_obj_collections:
        if len(course['faculty_url']) != 0:
            course['faculty_page_obj'] = parse_page_to_obj(course['faculty_url'])
            print(f"{course['course_name']} faculty page has been parsed")
    faculty_origin_list = []
    # get faculty info
    for course in course_name_url_obj_collections:
        if len(course['faculty_url']) != 0:
            faculty = get_faculty_info(course['faculty_page_obj'])
            print(f"{course['course_name']}'s faculty info parsed")
            faculty_origin_list += faculty

    # get rid of all the repetitions by checking repeating names in faculty_origin_list
    faculty_names = set()
    faculty_final_list = []
    for faculty_info in faculty_origin_list:
        if faculty_info['name'] not in faculty_names:
            faculty_names.add(faculty_info['name'])
            faculty_final_list.append(faculty_info)

    write_category_list_to_json(faculty_final_list, '../outputfiles/FACULTY_LIST_3399_EUR_0910.json')












if __name__ == "__main__":
    main()

