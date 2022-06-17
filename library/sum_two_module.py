#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2020, Bianca Henderson <beeankha@gmail.com>
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
    - Practicing writing a module.
options:
    number_one:
      description:
        - The first integer that's given.
      required: False
      type: str
      default: "0"
    number_two:
      description:
        - The second integer that's given.
      required: False
      type: str
      default: "1"
'''

EXAMPLES = '''
- name: "Add two numbers"
  sum_module:
    number_one: 3
    number_two: 5
  register: sum_results

- debug:
    var: sum_results
'''

from ansible.module_utils.basic import AnsibleModule

def main():

    argument_spec = dict(
        number_one=dict(required=False, default='0', type='str'),
        number_two=dict(required=False, default='1', type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    number_one = module.params.get('number_one')
    number_two = module.params.get('number_two')

    try:
        json_output = {'sum': (int(number_one) + int(number_two))}
    except ValueError:
        module.fail_json(msg="You didn't pass in sum-able integers!")

    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
