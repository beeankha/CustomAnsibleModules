#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2020, Bianca Henderson <bianca@redhat.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}


DOCUMENTATION = '''
---
module: sum_module
author: "Bianca Henderson (@beeankha)"
version_added: "2.9"
short_description: A way to add two numbers together.
description:
    - A module that sums.
options:
    numbers:
      description:
        - A list of integers to add.
      required: True
      type: list
      default: None
'''

EXAMPLES = '''
- name: "Add three numbers"
  sum_module:
    numbers: [3, 5, 9]
  register: sum_results

- debug:
    var: sum_results
'''

from ansible.module_utils.basic import AnsibleModule

def main():

    argument_spec = dict(
        numbers=dict(required=True, default=None, type='list'),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    numbers = module.params.get('numbers')
    sum_of_numbers = sum(numbers)

    try:
        json_output = {'sum': int(sum_of_numbers)}
    except ValueError:
        module.fail_json(msg="You didn't pass in sum-able integers!")

    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
