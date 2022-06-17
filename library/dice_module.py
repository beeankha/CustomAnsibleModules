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
module: dice_module
author: "Bianca Henderson (@beeankha)"
version_added: "2.9"
short_description: The silliest way to roll some dice!
description:
    - A way to roll digital dice via Ansible playbook.
options:
    dice_side_number:
      description:
        - Customize the number of sides for the die you roll.
      required: False
      type: int
      default: 20
    number_of_rolls:
      description:
        - Choose how many times you want to roll the custom die.
      required: False
      type: int
      default: 1
'''

EXAMPLES = '''
- name: "Roll some dice"
  dice_module:
    dice_side_number: 12
    number_of_rolls: 5
  register: roll_result

- debug:
    var: roll_result
'''

import random
import json

from ansible.module_utils.basic import AnsibleModule


def custom_dice_roll(dice_side_number, number_of_rolls):
    dice_roll_results = []
    for _ in range(number_of_rolls):
        dice_roll_results.append(random.randint(1,int(dice_side_number)))
    return dice_roll_results

def main():
    argument_spec = dict(
        dice_side_number=dict(required=False, default=20, type='int'),
        number_of_rolls=dict(required=False, default=1, type='int'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    dice_side_number = module.params.get('dice_side_number')
    number_of_rolls = module.params.get('number_of_rolls')

    try:
        json_output = {'custom_roll_result': custom_dice_roll(dice_side_number, number_of_rolls)}
    except ValueError:
        module.fail_json(msg='This module parameter takes an integer!')

    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
