import re
import bs4


def remove_branch(start_element: bs4.element.Tag):
    if start_element.name is None:
        return
    current_element = start_element
    while len(current_element.parent.find_all(recursive=False)) == 1:
        current_element = current_element.parent
    current_element.decompose()


def has_unwrapped_content(element: bs4.element.Tag):
    return len(get_unwrapped_strings(element)) > 0 and not is_element_content_tag(element)


def get_unwrapped_strings(current_element: bs4.element.Tag):
    unwrapped_strings = current_element.find_all(text=True, recursive=False)
    return list(filter(lambda string: string != "", map(lambda string: string.strip(), unwrapped_strings)))


def find_all_structures(start_element: bs4.element.Tag):
    elements = start_element.find_all(
        lambda tag: len(tag.find_previous_siblings()) == 0 and is_alternating_element(tag) and len(tag.parent.find_all(recursive=False)) >= 3)
    return list(map(lambda element: element.parent, elements))


def is_alternating_element(start_element: bs4.element.Tag):
    children = start_element.find_all(recursive=False)
    return len(children) == 1 and len(children[0].find_all(recursive=False)) == 0


def is_element_content_tag(element: bs4.element.Tag):
    return element.name in state['content_tags']


def get_all_link_elements(soup):
    all_links = soup.find_all('a')
    return [link.get('href') for link in all_links if link is not None]


def is_valid_relative_path(path: str):
    return path.startswith("/") and not bool(re.search(r"\.[a-zA-Z0-9]+$", path)) and not path.endswith("/yahoo")


state = {
    "normalize_text_tags": ['br', 'em', 'strong', 'i', 'b'],
    "unwanted_tags": ['img', 'svg', 'picture', 'script', 'source', 'iframe', 'style', 'link', 'sup'],
    "content_tags": ['p', 'a'] + [f'h{i + 1}' for i in range(10)]
}
