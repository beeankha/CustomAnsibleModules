## Custom Ansible Modules

Some custom modules I've written to expand my use of Ansible.


### Module Descriptions


#### `sum_module.py`

Adds a list of numbers together.


#### `dice_module.py`

The ~worst~ BEST way ever to roll dice! 😁

Customize the number of sides you want your die to have (defaults to `20`), as well as the number of times you want to roll it (defaults to `1`).

#### `hn_top_stories.py`

Gather data on the top `N` number of stories on [Hacker News](https://news.ycombinator.com/news).

Select the number of top stories via the `number_of_entries` parameter. Optional outputs include `story_id`, `author`, and `comments` (the number of comments the article has). Output is sorted by upvotes, with most upvoted at the top.

[Based on this Python script](https://github.com/beeankha/SimplePythonStuff/blob/main/Baby'sFirstDataScience/hn_submissions.py)

A more in-depth example of this module can be found [here](https://github.com/thenets/study-ansible/blob/main/how-to-create-a-module/library/get_news.py).

> **NOTE:** This module requires `requests`.

* * *

### How to Use

A practice playbook is provided in this repo (`practice_playbook.yml`).

Clone/download these files locally, then use your terminal to `cd` into the `Custom_Ansible_Modules` directory.  Once there, run:

```
ansible-playbook practice_playbook.yml
```

...and that's it!  If everything is working correctly, then output like what's shown below should appear on your terminal:

![Playbook Output](images/NewDiceRollOutput.png)
