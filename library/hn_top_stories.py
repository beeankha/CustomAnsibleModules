#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2022, Bianca Henderson <beeankha@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}


DOCUMENTATION = '''
---
module: hn_top_stories
author: "Bianca Henderson (@beeankha)"
version_added: "2.9"
short_description: Hacker News API data gathering
description:
    - A way to display data from the top stories on Hacker News API.
options:
    number_of_entries:
      description:
        - Number of entries to look at.
      required: False
      type: int
      default: 1
    story_id:
      description:
        - Select if story ID should be displayed.
        required: False
        type: bool
        default: False
    author:
      description:
        - Shows name of author.
        required: False
        type: bool
        default: False
    comments:
      description:
        - Select if number of comments should be displayed.
        required: False
        type: bool
        default: False
'''

EXAMPLES = '''
- name: "Hacker News API Call"
  hn_top_stories:
    number_of_entries: 30
    story_id: True
  register: top_stories
  # the above outputs the module register into a variable, then you can
  # print out that info via debug (below)
- debug:
    var: top_stories
'''

from ansible.module_utils.basic import AnsibleModule
from collections import OrderedDict
from operator import itemgetter

import requests


def api_scrape_result(number_of_entries, story_id, author, comments):
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    print(f"Status code: {r.status_code}")

    # Process information about each submission.
    submission_ids = r.json()[:number_of_entries]
    submission_dicts = []
    for submission_id in submission_ids:

        # Make a separate API call for each submission.
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        print(f"id: {submission_id}\tstatus: {r.status_code}")
        response_dict = r.json()

        # Build a dictionary for each article.
        submission_dict = {
            'title': response_dict['title'],
            'score': response_dict['score'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
        }

        # Add optional parameters
        if story_id:
            id_entry = {'story_id': response_dict['id']}
            submission_dict.update(id_entry)
        if author:
            show_author = {'author': response_dict['by'],}
            submission_dict.update(show_author)
        if comments:
            comment_number = {'comments': response_dict.get('descendants', 0)}
            submission_dict.update(comment_number)

        submission_dicts.append(submission_dict)

        # Output is sorted by number of upvotes
        submission_dicts = sorted(submission_dicts, key=itemgetter('score'), reverse=True)

    return submission_dicts


def main():
    argument_spec = dict(
        number_of_entries=dict(required=False, default=1, type='int'),
        story_id=dict(required=False, default=False, type='bool'),
        author=dict(required=False, default=False, type='bool'),
        comments=dict(required=False, default=False, type='bool'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    number_of_entries = module.params.get('number_of_entries')
    story_id = module.params.get('story_id')
    author = module.params.get('author')
    comments = module.params.get('comments')

    try:
        json_output = {'top_hn_submissions': api_scrape_result(number_of_entries, story_id, author, comments)}
    except ValueError:
        module.fail_json(msg="Something went wrong!")

    module.exit_json(**json_output)

if __name__ == '__main__':
    main()
