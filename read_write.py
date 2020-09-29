import csv
import json


def write_category_list_to_csv(categories,file_name):
    lst = []
    with open(file_name, mode='w') as categories_file:
             category_writer = csv.writer(categories_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             category_writer.writerow(['category_name', 'category_url','parent_url'])
             for category in categories:
                 category_writer.writerow(category)


# write categories to json file
def write_category_list_to_json(categories,file_name):
    with open(file_name, 'w') as cp:
        json.dump(categories, cp)


def write_course_list_to_json(course_info_list,file_name):
    with open(file_name, 'w') as cp:
        json.dump(course_info_list, cp)