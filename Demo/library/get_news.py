#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2022, Luiz Felipe F M Costa <luiz@thenets.org>
#           Bianca Henderson <beeankha@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: get_news
author: "Luiz Felipe F M Costa (@thenets), Bianca Henderson (@beeankha)"
version_added: "2.9"
short_description: The silliest way to get the news from Hacker News
description:
    - Get news in Ansible and HTML output format.
options:
    number_of_news:
      description:
        - The number of news you want to get from Hacker News.
      required: False
      type: int
      default: 10
'''

EXAMPLES = '''
- name: "Get news"
    get_news:
    number_of_news: 5
    register: news_results
- debug:
    var: news_results.news
- debug:
    var: news_results.news_html
'''

RETURN = '''
news:
    description: The news you requested.
    type: list
    returned: always
news_html:
    description: The news you requested in HTML format.
    type: list
    returned: always
count:
    description: Number of news returned.
    type: int
    returned: always
    sample: 10
'''

import requests
import datetime

from ansible.module_utils.basic import AnsibleModule

def _get_news_list_ids(number_of_news) -> list:
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    result = requests.get(api_url)
    return result.json()[:number_of_news]

def _get_news(news_id) -> dict:
    api_url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(news_id)
    result = requests.get(api_url)
    return result.json()

def _parse_to_html_news(news):
    pretty_date = datetime.datetime.fromtimestamp(news["time"]).strftime('%Y-%m-%d %H:%M:%S')
    return f"""
    <li>
        <a href="https://news.ycombinator.com/item?id={news['id']}">{news['title']}</a>
        <p>{news['type']}</p>
        <p>{news['score']} points</p>
        <p>by {news['by']}</p>
        <p>{pretty_date}</p>
    </li>
    """

def module_get_news(number_of_news: int) -> dict:
    news_ids = _get_news_list_ids(number_of_news)
    news_list = []
    news_html_list = []
    for news_id in news_ids:
        news_list.append(_get_news(news_id))
        news_html_list.append(_parse_to_html_news(news_list[-1]))

    return {
        "news": news_list,
        "news_html": news_html_list,
    }

def main():
    argument_spec = dict(
        number_of_news=dict(required=False, default=10, type='int'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    number_of_news = module.params.get('number_of_news')

    try:
        output = module_get_news(number_of_news)
    except ValueError:
        module.fail_json(msg="Oh, something went wrong! And I don't know how to write a proper error message.")

    module.exit_json(**output)

if __name__ == '__main__':
    main()
