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
            print("{name} -> {value}".format(**event_data))

        time.sleep(0.001)
```


**As a base `class`**


```Python
#!/usr/bin/env python3


import time

from lib.modules.xjoypad import XJoypad


class Custom_XJoypad(XJoypad):
    """
    Custom_XJoypad extends XJoypad, adds support for normalizing event values and dead-zone zeroing
    """

    def __init__(self, device_index = 0, amend_settings = None, **kwargs):
        if isinstance(amend_settings, dict):
            super(Custom_XJoypad, self).__init__(
                device_index = device_index,
                amend_settings = amend_settings,
                **kwargs)
        else:
            super(Custom_XJoypad, self).__init__(
                device_index = device_index,
                amend_settings = {
                    'axes': {
                        evdev.ecodes.ABS_X: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': -90, 'max': 90},
                            'dead_zone': {'above': -10, 'bellow': 10},
                        },
                        evdev.ecodes.ABS_Y: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': -90, 'max': 90},
                            'dead_zone': {'above': -10, 'bellow': 10},
                        },
                        evdev.ecodes.ABS_Z: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': -90, 'max': 90},
                            'dead_zone': {'above': -10, 'bellow': 10},
                        },
                        evdev.ecodes.ABS_RZ: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': -90, 'max': 90},
                            'dead_zone': {'above': -10, 'bellow': 10},
                        },
                        evdev.ecodes.ABS_BRAKE: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': 0, 'max': 180},
                            'dead_zone': {'above': 0, 'bellow': 10},
                        },
                        evdev.ecodes.ABS_GAS: {
                            'absolute_bounds': {'min': 0, 'max': 255},
                            'normalize_bounds': {'min': 0, 'max': 180},
                            'dead_zone': {'above': 0, 'bellow': 10},
                        },
                    },
                },
                **kwargs)

    def axis_callback(self, event):
        """
        Thanks be to -- [Normalizing data to certain range of values](https://stackoverflow.com/questions/48109228/)
        """
        _axis = self['axes'][event.code]
        _event_data = super(Custom_XJoypad, self).axis_callback(event)
        _absolute_bounds = _axis['absolute_bounds']
        _normalize_bounds = _axis['normalize_bounds']

        _normalized_value = _normalize_bounds['min'] + (
            event.value - _absolute_bounds['min']
        ) * (
            _normalize_bounds['max'] - _normalize_bounds['min']
        ) / (
            _absolute_bounds['max'] - _absolute_bounds['min']
        )

        _dead_zone_above = _axis['dead_zone']['above']
        _dead_zone_bellow = _axis['dead_zone']['bellow']
        if _normalized_value < _dead_zone_bellow and _normalized_value > _dead_zone_above:
            _normalized_value = 0

        _event_data.update({'normalized_value': _normalized_value})
        _axis['last_event'] = _event_data
        return _event_data

    def button_callback(self, event):
        _button = self['buttons'][event.code]
        _event_data = super(Custom_XJoypad, self).button_callback(event)

        if event.value == 0:
            _normalized_value = 'released'
        elif event.value == 1:
            _normalized_value = 'pressed'
        elif event.value == 2:
            _normalized_value = 'held'

        _event_data.update({'normalized_value': _normalized_value})
        _button['last_event'] = _event_data
        return _event_data

    def dpad_callback(self, event):
        _dpad = self['dpad'][event.code]
        _event_data = super(Custom_XJoypad, self).dpad_callback(event)

        if evdev.ecodes.ABS_HAT0X == event.code:
            if event.value == 0:
                if _dpad['last_event']['value'] == -1:
                    _normalized_value = 'released-left'
                elif _dpad['last_event']['value'] == 1:
                    _normalized_value = 'released-right'
                else:
                    _normalized_value = 'released-left-right'
            elif event.value == -1:
                _normalized_value = 'pressed-left'
            elif event.value == 1:
                _normalized_value = 'pressed-right'

        elif evdev.ecodes.ABS_HAT0Y == event.code:
            if event.value == 0:
                if _dpad['last_event']['value'] == -1:
                    _normalized_value = 'released-up'
                elif _dpad['last_event']['value'] == 1:
                    _normalized_value = 'released-down'
                else:
                    _normalized_value = 'released-up-down'
            elif event.value == -1:
                _normalized_value = 'pressed-up'
            elif event.value == 1:
                _normalized_value = 'pressed-down'

        _event_data.update({'normalized_value': _normalized_value})
        _dpad['last_event'] = _event_data
        return _event_data


if __name__ == '__main__':
    import time

    xjoypad = Custom_XJoypad()
    for event_data in xjoypad:
        if event_data:
            print("Event name -> {event_name} {value} {normalized_value}".format(
                event_name = event_data['name'],
                value = event_data['value'],
                normalized_value = event_data.get('normalized_value'),
            ))

        time.sleep(0.001)

```


> As of versions `v0.0.2` or greater, `XJoypad` returns event data with `normalized_value` key value pares set similar to above, and with better generalization.


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
