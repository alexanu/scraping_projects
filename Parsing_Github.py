# $ pip install PyGithub
# PyGithub documentation: https://buildmedia.readthedocs.org/media/pdf/pygithub/stable/pygithub.pdf


from github import Github
import pandas as pd
import os

# The config with tokens is located in the folder which is on the same hierarchy level as current folder
'''
Path_To_TKNS = os.path.join(os.path.abspath(os.path.join(os.getcwd(),"../..")), "Python_Trading_Snippets","connections.cfg")

from configparser import ConfigParser
config = ConfigParser()
config.read(Path_To_TKNS)
GHLogin=config['GitHub']['Login']
GHpswrd=config['GitHub']['Password']
'''
g = Github('a6df65e1af43e87f2e587c2644bb2f88e45a6d11')


#-------- Parsing my repos --------------------------------------------------------------

ID_my=[]
Parent_name=[]
Parent_id=[]
Parent_update=[]
descr_my=[]
Repo_source=[]
created_my=[]
size_my=[]
own_repo = "Own repo"

for repo in g.get_user().get_repos(): # going throung my repos
    ID_my.append(repo.id)
    if repo.parent is None: # if the repo is mine (i.e. no parent)
        Parent_name.append(repo.name)
        Parent_id.append(repo.id)
        Parent_update.append(repo.updated_at)
        Repo_source.append("Own")
    else:
        Parent_name.append(repo.parent.full_name)
        Parent_id.append(repo.parent.id)
        Parent_update.append(repo.parent.updated_at)
        Repo_source.append("Forked")
    descr_my.append(repo.description)
    created_my.append(repo.created_at)
    size_my.append(repo.size)
    
for repo in g.get_user().get_starred(): # going through starred repos
    ID_my.append(repo.id)
    Parent_name.append(repo.name)
    Parent_id.append(repo.id) # the same as ID_my
    Parent_update.append(repo.updated_at)
    Repo_source.append("Star")
    descr_my.append(repo.description)
    created_my.append(repo.created_at)
    size_my.append(repo.size)
    
my_repos = pd.DataFrame({
                    'My_ID': ID_my,
                    'Source': Repo_source,
                    'Parent': Parent_name,
                    'Parent_ID': Parent_id,
                    'Parent_Update': Parent_update,
                    'Created': created_my,
                    'Size': size_my,
                    'Descrip': descr_my})

my_repos.to_csv("Repos.csv")

#-------- Searching Github --------------------------------------------------------------

from df2gspread import gspread2df as g2d

from df2gspread import df2gspread as d2g

d2g.upload(pr_instr, gfile='/Trading FXCM/PyData', wks_name='pr_instr')
weights = g2d.download(gfile="1bmy2DLu5NV5IP-mo9rGWOyHOx7bEfoglVZmzzuHi5zc", wks_name="Weights", col_names=True, row_names=True, credentials=None, start_cell='A1')





keywords_all = "IEX, hedge, oanda, quandl, NYSE, ETF, " \
            "market calendar, equity, kelly, arbitrage, backtest, " \
            "quant, EDGAR, del Prado, zorro trading"
keywords = [keyword.strip() for keyword in keywords_all.split(',')]

# exclude_keywords = "ng-zorro, ngx-zorro, ngzorro, CSS, Typescript"
# exclude_keyword = [keyword.strip() for keyword in exclude_keywords.split(',')]
# query = '+'.join(keyword) + '+NOT'+ '+'.join(exclude_keyword)+'pushed:>=2019-07-05'+'language:python' +'+in:readme+in:description'
# result = g.search_repositories(query, 'stars', 'desc')


ID_my=[]
Parent_name=[]
Parent_id=[]
Parent_update=[]
descr_my=[]
Repo_source=[]
created_my=[]


for keyword in keywords:
    repositories = g.search_repositories(query=keyword+' language:python in:name in:readme in:description pushed:>2020-05-21', sort='updated')
    print(f'Found {repositories.totalCount} repo(s) for key={keyword}')
    for repo in repositories:
        ID_my.append(repo.id)
        Parent_name.append(repo.name)
        Parent_id.append(repo.id)
        Parent_update.append(repo.updated_at)
        created_my.append(repo.created_at)
        descr_my.append(repo.description)

Search_result = pd.DataFrame({'My_ID': ID_my,
                            'Parent': Parent_name,
                            'Parent_ID': Parent_id,
                            'Parent_Update': Parent_update,
                            'Created': created_my,
                            'Descrip': descr_my,
				    		})
Search_result.to_csv("GH_Search_Results.csv")


#################################################################################
# Getting all trending repos from GH

    import bs4
    import requests

    ignore = ["python/cpython"]

    fmt = """  echo ; echo -n "{i} flake8 testing of {long} on " ; python -V
    - git clone --depth=50 --branch=master https://github.com/{long} ~/{short}
    - cd ~/{short}
    # stop the build if there are Python syntax errors or undefined names
    - flake8 . --count --exit-zero --select=E9,F63,F7,F82 --statistics
    # exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
    - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    """

    url = "https://github.com/trending?l=Python"
    soup = bs4.BeautifulSoup(requests.get(url).content, "lxml")  # or 'html5lib'
    # 'python / cpython'
    repos = soup.find("ol", class_="repo-list").find_all("a", href=True)
    # 'python/cpython'
    repos = (r.text.strip().replace(" ", "") for r in repos if "/" in r.text)
    # {'i', 7, 'long': 'python/cpython', 'short': 'cpython'}
    repos = (
        {"i": i + 1, "long": repo, "short": repo.split("/")[-1]}
        for i, repo in enumerate(repos)
    )
    print("=" * 50)
    print("\n".join(fmt.format(**repo) for repo in repos if repo not in ignore))

    # -------------------------------------------------------------------------------------------------

    url = "https://github.com/trending?l=Python"
    soup = bs4.BeautifulSoup(requests.get(url).content, "lxml")  # or 'html5lib'
    repos = soup.find("ol", class_="repo-list").find_all("a", href=True)
    repos = (r.text.strip().replace(" ", "") for r in repos if "/" in r.text)
    print("\n".join(repos))

################################################################################################

import time
import json
import requests
from db import REDIS

REPO_SHOW = '1'
REPO_HIDDEN = '0'

SEARCH_API = 'https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%s'


def search_github(keyword):
    for i in range(1, 21):
        res = requests.get(SEARCH_API % (keyword, i))
        repo_list = res.json()['items']
        for repo in repo_list:
            repo_name = repo['html_url']
            desc = {
                'repo_desc': repo['description'],
                'star': repo['stargazers_count'],
                'is_show': REPO_SHOW
            }
            if REDIS.hsetnx('repos', repo_name, json.dumps(desc)):
                print repo_name
        time.sleep(10)


if __name__ == '__main__':
    keywords = ['spider', 'crawl']
    REDIS.set('keywords', ' '.join(keywords))
    for keyword in keywords:
        search_github(keyword)

################################################################################################

import requests, time, datetime, sys
from dateutil.relativedelta import relativedelta


def main(args):
    dummy_dict = {}
    for arg in args:
        if '=' in arg:
            split = arg.split('=')
            dummy_dict[split[0]] = split[1]
    args = dummy_dict

    if 'github_id' not in args or 'github_id' not in args:
        print('Required parameters are missing.')
        exit(-1)

    # init
    github_api_url = 'https://api.github.com'
    github_id = args['github_id']
    github_token = args['github_token']

    search_topic = args.get('search_topic', 'hacktoberfest')
    search_month_range = int(args.get('search_month_range', 6))
    search_location = args.get('search_location', 'Korea')
    my_auth = (github_id, github_token)

    now_datetime = datetime.datetime.now()
    limit_datetime = relativedelta(months=-search_month_range) + now_datetime

    while now_datetime > limit_datetime:
        page = 1
        while True:
            search_base_time = str(now_datetime.strftime('%Y-%m-%d'))
            topics = requests.get(url=github_api_url + f'/search/repositories?q=topic:{search_topic}+created:{search_base_time}&page={page}',
                                  auth=my_auth,
                                  headers={'Accept': 'application/vnd.github.mercy-preview+json'}).json()
            time.sleep(5)
            # https://docs.github.com/en/free-pro-team@latest/rest/reference/search
            # To satisfy that need, the GitHub Search API provides up to 1,000 results for each search.
            if int(len(topics['items'])) == 0:
                break

            print(
                f'search base time : {search_base_time}, ',
                f'now time : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, ',
                f'page : {page}, ',
                f'user_count : {len(topics["items"])}, ',
                f'total_count : {topics["total_count"]}'
            )

            for topic in topics['items']:
                user_id=topic['owner']['login']
                user = requests.get(url=github_api_url + f'/users/{user_id}', auth=my_auth).json()
                time.sleep(0.5)
                # https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#rate-limiting
                # For API requests using Basic Authentication or OAuth, you can make up to 5,000 requests per hour.

                if 'location' in user and user['location'] is not None and search_location in user['location']:
                    print(f'Found it! = createdat : {topic["created_at"]}, repository : {topic["html_url"]}')

            page = page + 1

        now_datetime = now_datetime + datetime.timedelta(days=-1)


if __name__ == "__main__":
    main(sys.argv)