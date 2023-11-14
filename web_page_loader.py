import concurrent.futures
import threading
import requests
from bs4 import BeautifulSoup
import atexit


class WebPageLoader:
    def __init__(self, base_url):
        self.base_url = base_url
        self.web_page_dict = {}
        self.event_dict = {}
        self.noop_element = BeautifulSoup("", 'html.parser')

    def _process_url(self, url_path):
        self.web_page_dict[url_path] = self.noop_element
        try:
            response = requests.get(self.base_url + url_path)
            html_content = response.text
            self.web_page_dict[url_path] = BeautifulSoup(html_content, 'html.parser')
        except Exception:
            pass
        finally:
            del tasks[url_path]
            self.event_dict[url_path].set()

    def add_url(self, url_path):
        self.event_dict[url_path] = threading.Event()
        task = executor.submit(self._process_url, url_path)
        tasks[url_path] = task

    def get_url(self, url_path):
        if self.event_dict[url_path].wait(timeout=15):
            return self.web_page_dict[url_path]
        print("failed " + url_path)
        return BeautifulSoup("", 'html.parser')


def end_tasks():
    for task in tasks.values():
        task.cancel()


def cleanup(*args):
    executor.shutdown(wait=False, cancel_futures=True)


executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
tasks = {}
atexit.register(cleanup)
