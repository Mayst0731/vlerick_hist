from scrapingfiles.parse_pages import parse_page_to_obj
from urllib import parse


def get_all_categories(url):

    cate_dict = dict()
    category_page_obj = parse_page_to_obj(url)
    category_divs = category_page_obj.find_all('div',attrs={'class':'grid_8'})
    category_divs += category_page_obj.find_all('div', attrs={'class': 'grid_8 omega'})
    category_divs += category_page_obj.find_all('div', attrs={'class': 'grid_8 alpha'})

    check_repeat = set()

    for category_info in category_divs:
        category_name = category_info.find('h2').text
        prefix = category_info.parent.previous_sibling.previous_sibling.previous_sibling.h3.text.strip()
        if category_name not in check_repeat:
            category_name = prefix + ' - ' + category_name
            check_repeat.add(category_name)
            category_url_post = category_info.find('ul').find('a').get('href')
            category_url = parse.urljoin(url, category_url_post)
            cate_dict[category_name] = category_url

    return cate_dict







