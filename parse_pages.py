from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp

def parse_page_to_obj(url):
    try:
        html_content = requests.get(url).content
        soup = BeautifulSoup(html_content, features='lxml')
    except Exception as e:
        print(f"{url} was not parsed:\n {e}")
        return None
    return soup









