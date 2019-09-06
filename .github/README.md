# XJoypad
[heading__title]:
  #xjoypad
  "&#x2B06; Top of ReadMe File"


XJoypad is a Python2/3 iterator and wrapper API of `evdev`, for reading and parsing joypad and game-controller input events.


## [![Byte size of __init__.py][badge__master__xjoypad__source_code]][xjoypad__master__source_code] [![Open Issues][badge__issues__xjoypad]][issues__xjoypad] [![Open Pull Requests][badge__pull_requests__xjoypad]][pull_requests__xjoypad] [![Latest commits][badge__commits__xjoypad__master]][commits__xjoypad__master]



------


#### Table of Contents


- [:arrow_up: Top of ReadMe File][heading__title]

- [:zap: Quick Start][heading__quick_start]

  - [:memo: Edit Your ReadMe File][heading__your_readme_file]
  - [:snake: Utilize XJoypad][heading__utilize]
  - [:floppy_disk: Commit and Push][heading__commit_and_push]

- [&#x1F5D2; Notes][heading__notes]

- [&#x2696; License][heading__license]


------



## Quick Start
[heading__quick_start]:
  #quick-start
  "&#9889; Perhaps as easy as one, 2.0,..."


**Bash Variables**


```Bash
_module_name='xjoypad'
_module_https_url="https://github.com/python-utilities/${_module_name}.git"
_module_relative_path="lib/modules/${_module_name}"
```


**Bash Submodule Commands**


```Bash
cd "<your-git-project-path>"

git checkout master
mkdir -vp "lib/modules"

git submodule add\
 -b master --name "${_module_name}"\
 "${_module_https_url}" "${_module_relative_path}"
```


### Your ReadMe File
[heading__your_readme_file]:
  #your-readme-file
  "&#x1F4DD; Suggested additions for your ReadMe.md file so everyone has a good time with submodules"


Suggested additions for your _`ReadMe.md`_ file so everyone has a good time with submodules


```MarkDown
Install Python dependencies


    pip3 install --user evdev


Clone with the following to avoid incomplete downloads


    git clone --recurse-submodules <url-for-your-project>


Update/upgrade submodules via


    git submodule update --init --merge --recursive
```


### Utilize XJoypad
[heading__utilize]:
  #utilize-xjoypad
  "&#x1F40D; How to make use of this submodule within another project"


**As an `import`**


```Python
#!/usr/bin/env python3


from lib.modules.xjoypad import XJoypad


if __name__ == '__main__':
    import time

    xjoypad = XJoypad()
    for event_data in xjoypad:
        if event_data:
            print("{name} --> {value} --> {normalized_value}".format(**event_data))

        time.sleep(0.001)
```


**As a base `class`**


```Python
#!/usr/bin/env python3


import time

from lib.modules.xjoypad import XJoypad


class XJoypad_Buffer(XJoypad):
    """Extends `XJoypad` class with buffer and timeout features"""

    def __init__(self, device_index = 0, amend_settings = None, **kwargs):
        """
        Use `amend_settings` to modify select `self['sleeps']` settings
        """
        self['sleeps'] = {
            'min': 0.001,
            'max': 0.01,
            'acceleration': 0.001,
            'timeout': 120,
            'current': 0.001,
        }

        super(XJoypad_Buffer, self).__init__(device_index = device_index, amend_settings = amend_settings, **kwargs)

    def next(self):
        """
        Throws `GeneratorExit` if timeout is set and reached, otherwise returns `event_data` when available
        """
        while 1:
            _event_data = super(XJoypad_Buffer, self).next()
            if _event_data:
                self['sleeps']['slept_start'] = None
                self['sleeps']['current'] = self['sleeps']['min']
                return _event_data

            if not self['sleeps'].get('slept_start'):
                self['sleeps']['slept_start'] = time.time()

            if self['sleeps']['current'] < self['sleeps']['max']:
                self['sleeps']['current'] += self['sleeps']['acceleration']

            if self['sleeps'].get('timeout') and self['sleeps'].get('slept_last'):
                if self['sleeps']['slept_last'] - self['sleeps']['slept_start'] > self['sleeps']['timeout']:
                    self.throw(GeneratorExit)

            self['sleeps']['slept_last'] = time.time()
            time.sleep(self['sleeps']['current'])


if __name__ == '__main__':
    xjoypad = XJoypad_Buffer()
    for event_data in xjoypad:
        print("Event name -> {name} -- {value} -- {normalized_value}".format(**event_data))
        time.sleep(0.001)
```


### Commit and Push
[heading__commit_and_push]:
  #commit-and-push
  "&#x1F4BE; It may be just this easy..."


```Bash
git add .gitmodules
git add lib/modules/xjoypad


## Add any changed files too


git commit -F- <<'EOF'
:heavy_plus_sign: Adds `python-utilities/xjoypad#1` submodule

# ... anything else noteworthy
EOF


git push origin master
```


**:tada: Excellent :tada:** your repository is now ready to begin unitizing code from this project!


___


## Notes
[heading__notes]:
  #notes
  "&#x1F5D2; Additional resources and things to keep in mind when developing"


Pull Requests are welcome for fixing bugs and/or adding features.


___


## License
[heading__license]:
  #license
  "&#x2696; Legal bits of Open Source software"


Legal bits of Open Source software


```
XJoypad ReadMe documenting how things like this could be utilized
Copyright (C) 2019  S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation; version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```



[badge__commits__xjoypad__master]:
  https://img.shields.io/github/last-commit/python-utilities/xjoypad/master.svg

[commits__xjoypad__master]:
  https://github.com/python-utilities/xjoypad/commits/master
  "&#x1F4DD; History of changes on this branch"


[xjoypad__community]:
  https://github.com/python-utilities/xjoypad/community
  "&#x1F331; Dedicated to functioning code"


[xjoypad__gh_pages]:
  https://github.com/python-utilities/xjoypad/tree/gh-pages
  "Source code examples hosted thanks to GitHub Pages!"



[badge__demo__xjoypad]:
  https://img.shields.io/website/https/python-utilities.github.io/xjoypad/index.html.svg?down_color=darkorange&down_message=Offline&label=Demo&logo=Demo%20Site&up_color=success&up_message=Online

[demo__xjoypad]:
  https://python-utilities.github.io/xjoypad/index.html
  "&#x1F52C; Check the example collection tests"


[badge__issues__xjoypad]:
  https://img.shields.io/github/issues/python-utilities/xjoypad.svg

[issues__xjoypad]:
  https://github.com/python-utilities/xjoypad/issues
  "&#x2622; Search for and _bump_ existing issues or open new issues for project maintainer to address."


[badge__pull_requests__xjoypad]:
  https://img.shields.io/github/issues-pr/python-utilities/xjoypad.svg

[pull_requests__xjoypad]:
  https://github.com/python-utilities/xjoypad/pulls
  "&#x1F3D7; Pull Request friendly, though please check the Community guidelines"


[badge__master__xjoypad__source_code]:
  https://img.shields.io/github/size/python-utilities/xjoypad/__init__.py.svg?label=__init__.py

[xjoypad__master__source_code]:
  https://github.com/python-utilities/xjoypad/blob/master/__init__.py
  "&#x2328; Project source, one Python file of importable code!"


[xjoypad__gh_pages]:
  https://github.com/python-utilities/xjoypad/tree/gh-pages
  "Source code examples hosted thanks to GitHub Pages!"
