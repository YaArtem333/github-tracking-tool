from bs4 import BeautifulSoup
import requests


class RepositoryParse:

    def __init__(self, account, repository):
        self.url = f'http://github.com/{account}/{repository}'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def get_numbers_tool(self, tag, _class):
        try:
            full_response = self.soup.find_all(tag, class_=_class)
            response_list = []
            digits = '1234567890.km'
            for res in full_response:
                modified_response = ''
                for symbol in res.text:
                    if symbol in digits:
                        modified_response += symbol
                response_list.append(modified_response)
            return response_list
        except:
            return "0"

    def get_branches(self):
        try:
            return self.get_numbers_tool('a', 'ml-3 Link--primary no-underline')[0]
        except:
            return "0"

    def get_tags(self):
        try:
            return self.get_numbers_tool('a', 'ml-3 Link--primary no-underline')[1]
        except:
            return "0"

    def get_commits(self):
        try:
            return self.get_numbers_tool('span', 'd-none d-sm-inline')[0][:-2]
        except:
            return "0"

    def get_stars(self):
        try:
            return self.get_numbers_tool('a', 'Link Link--muted')[1]
        except:
            return "0"

    def get_watching(self):
        try:
            return self.get_numbers_tool('a', 'Link Link--muted')[2]
        except:
            return "0"

    def get_forks(self):
        try:
            return self.get_numbers_tool('a', 'Link Link--muted')[3][:-1]
        except:
            return "0"
