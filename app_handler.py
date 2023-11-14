import threading
import time

import normalizer
import utils
from web_page_loader import WebPageLoader


base_url = 'https://www.h-brs.de'
url_path = '/de'
max_pages = 2000


def start_process():
    thread = threading.Thread(target=refresh_mirror)
    thread.daemon = True
    thread.start()


def refresh_mirror():
    while True:
        web_page_loader = WebPageLoader(base_url)
        web_page_loader.add_url(url_path)

        found_links = {url_path}
        url_list = [(url_path, 0)]
        index = 0
        normalized_pages_tmp = {}

        while index < len(url_list):
            current_url_path, depth = url_list[index]

            soup = web_page_loader.get_url(current_url_path)
            if soup is not None and soup.body is not None:
                normalizer.normalize_tree(soup)
                normalized_pages_tmp[current_url_path] = soup
                new_links = utils.get_all_link_elements(soup)

                for new_link in new_links:
                    if len(url_list) >= max_pages:
                        continue
                    if new_link is not None and new_link not in found_links and new_link != "":
                        found_links.add(new_link)
                        if utils.is_valid_relative_path(new_link):
                            url_list.append((new_link, depth + 1))
                            web_page_loader.add_url(new_link)

            index += 1
        global normalized_pages
        if len(normalized_pages) == 0:
            print("Finished initializing")
            print("Start-Url: " + url_path)
        normalized_pages = normalized_pages_tmp

        time.sleep(3600)


normalized_pages = {}
