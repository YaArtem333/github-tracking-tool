import requests
from bs4 import BeautifulSoup


class AccountParse:

    def __init__(self, account):
        self.url = f'http://github.com/{account}'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def get_repos_number(self):
        try:
            repos_number = self.soup.find('span', class_='Counter').text
            check = int(repos_number)
            return repos_number
        except:
            return "0"

    def get_repos(self):
        try:
            repos_list = []
            repos = self.soup.find_all('span', class_='repo')
            for repo in repos:
                repos_list.append(repo.text)
            check = list(repos_list)
            return repos_list
        except:
            return "0"

    def get_followers(self):
        try:
            followers = self.soup.find_all('span', class_='text-bold color-fg-default')
            follow_list = []
            for f in followers:
                follow_list.append(f.text)
            check = int(follow_list[0])
            return follow_list[0]
        except:
            return "0"

    def get_following(self):
        try:
            followers = self.soup.find_all('span', class_='text-bold color-fg-default')
            follow_list = []
            for f in followers:
                follow_list.append(f.text)
            check = int(follow_list[1])
            return follow_list[1]
        except:
            return "0"

    def get_contributions_last_year(self):
        try:
            full_response = self.soup.find('h2', class_='f4 text-normal mb-2').text
            contributions = ''
            digits = '1234567890'
            for symbol in full_response:
                if symbol in digits:
                    contributions+=symbol
            check = int(contributions)
            return contributions
        except:
            return "0"
