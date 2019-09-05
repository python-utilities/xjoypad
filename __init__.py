#!/usr/bin/env python


import evdev

from collections import Iterator


license = """
Python 2/3 `evdev` wrapper class for parsing Joypad input events.
Copyright (C) 2019 S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class XJoypad(dict, Iterator):
    """
    Python 2/3 dictionary iterator hybrid for reading Joypad events from evdev

    ## Example usage

        from time import sleep

        joy = XJoypad(device_index = 0)
        for event_data in joy:
            if event_data:
                print("{name} -> {value}".format(**event_data))

            sleep(0.001)

    See `.next()` method for how `event_data` dictionary is built.
    """

    def __init__(self, device_index = 0, amend_settings = None, **kwargs):
        """
        Initializes dictionary similar to following

            device: evdev.InputDevice(evdev.list_devices()[device_index])

            axes: {
                evdev.ecodes.ABS_X: {
                    'name': 'stick_left_x',
                    'callback': self.axis_callback,
                    'last_event': None,
                },
                # ...
            }

            buttons: {
                evdev.ecodes.BTN_A: {
                    'name': 'button_a',
                    'callback': self.button_callback,
                    'last_event': None,
                },
                # ...
            }

            dpad: {
                evdev.ecodes.ABS_HAT0X: {
                    'name': 'dpad_x',
                    'callback': self.dpad_callback,
                    'last_event': None,
                },
                # ...
            }

        ## Example customize

            import evdev


            def gas_callback(event):
                _axis = joy['axes'][event.code]
                _event_data = {
                    'code': event.code,
                    'name': _axis['name'],
                    'usec': event.usec,
                    'sec': event.sec,
                    'time': event.timestamp(),
                    'type': event.type,
                }

                if event.value > 25:
                    _event_data['value'] = event.value
                else:
                    _event_data['value'] = 0

                return _event_data


            joy = XJoypad(device_index = 0, amend_settings = {
                'axes': {
                    evdev.ecodes.ABS_GAS: {
                        'callback': gas_callback
                    }
                }
            })

        """
        self['device'] = evdev.InputDevice(evdev.list_devices()[device_index])

        self['axes'] = {
            evdev.ecodes.ABS_X: {
                'name': 'stick_left_x',
                'callback': self.axis_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_Y: {
                'name': 'stick_left_y',
                'callback': self.axis_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_Z: {
                'name': 'stick_right_x',
                'callback': self.axis_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_RZ: {
                'name': 'stick_right_y',
                'callback': self.axis_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_BRAKE: {
                'name': 'trigger_left',
                'callback': self.axis_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_GAS: {
                'name': 'trigger_right',
                'callback': self.axis_callback,
                'last_event': None,
            },
        }

        self['buttons'] = {
            evdev.ecodes.BTN_A: {
                'name': 'button_a',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_B: {
                'name': 'button_b',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_X: {
                'name': 'button_x',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_Y: {
                'name': 'button_y',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_TL: {
                'name': 'bumper_left',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_TR: {
                'name': 'bumper_right',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_START: {
                'name': 'button_start',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.KEY_BACK: {
                'name': 'button_select',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_THUMBL: {
                'name': 'thumb_left',
                'callback': self.button_callback,
                'last_event': None,
            },
            evdev.ecodes.BTN_THUMBR: {
                'name': 'thumb_right',
                'callback': self.button_callback,
                'last_event': None,
            },
        }

        self['dpad'] = {
            evdev.ecodes.ABS_HAT0X: {
                'name': 'dpad_x',
                'callback': self.dpad_callback,
                'last_event': None,
            },
            evdev.ecodes.ABS_HAT0Y: {
                'name': 'dpad_y',
                'callback': self.dpad_callback,
                'last_event': None,
            },
        }

        if isinstance(amend_settings, dict):
            XJoypad.merge(self, amend_settings)

        super(XJoypad, self).__init__(**kwargs)

    def __iter__(self):
        """
        This method plus `.next{}`/`__next__` and `.throw(...)` methods make this class iterable
        """
        return self

    @staticmethod
    def merge(target, amending_dict, path = None):
        """
        Merges amending_dict into target

        Thanks be to -- https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
        """
        if path is None:
            path = []

        for key in amending_dict.keys():
            if key in target.keys():
                if isinstance(target[key], dict) and isinstance(amending_dict[key], dict):
                    XJoypad.merge(target[key], amending_dict[key], path + [str(key)])
                elif target[key] == amending_dict[key]:
                    pass
                else:
                    # Overwrites pre-existing value
                    target[key] = amending_dict[key]
            else:
                target[key] = amending_dict[key]

        return target

    def axis_callback(self, event):
        """
        Sets `self['axes'][event.code]['last_event']` and returns dictionary parsed from `event`

        ## Example output

            {
                'code': event.code,         # `0` AKA `evdev.ecodes.ABS_X`
                'name': _axis['name'],      # `stick_left_x`
                'usec': event.usec,         # `211142L`
                'sec': event.sec,           # `4267000555L`
                'time': event.timestamp(),  # `4267000555.211142`
                'type': event.type,         # `3` AKA `evdev.ecodes.EV_ABS`
                'value': event.value,       # `0` to `255` for generic pads
            }
        """
        _axis = self['axes'][event.code]

        _event_data = {
            'code': event.code,
            'name': _axis['name'],
            'usec': event.usec,
            'sec': event.sec,
            'time': event.timestamp(),
            'type': event.type,
            'value': event.value,
        }

        _axis['last_event'] = _event_data
        return _event_data

    def button_callback(self, event):
        """
        Sets `self['buttons'][event.code]['last_event']` and returns dictionary parsed from `event`

        ## Example output

            {
                'code': event.code,         # `304` AKA `evdev.ecodes.BTN_A`
                'name': _button['name'],    # `button_a`
                'usec': event.usec,         # `211142L`
                'sec': event.sec,           # `4267000555L`
                'time': event.timestamp(),  # `4267000555.211142`
                'type': event.type,         # `1` AKA `evdev.ecodes.EV_KEY`
                'value': event.value,       # `1` Pressed, `0` Released, `2` Held
            }
        """
        _button = self['buttons'][event.code]

        _event_data = {
            'code': event.code,
            'name': _button['name'],
            'usec': event.usec,
            'sec': event.sec,
            'time': event.timestamp(),
            'type': event.type,
            'value': event.value,
        }

        _button['last_event'] = _event_data
        return _event_data

    def dpad_callback(self, event):
        """
        Sets `self['dpad'][event.code]['last_event']` and returns dictionary parsed from `event`

        ## Example output

            {
                'code': event.code,         # `16` or `17` AKA `evdev.ecodes.ABS_HAT0X` and `.ABS_HAT0Y`
                'name': _dpad['name'],      # `dpad_x` or `dpad_y`
                'usec': event.usec,         # `211142L`
                'sec': event.sec,           # `4267000555L`
                'time': event.timestamp(),  # `4267000555.211142`
                'type': event.type,         # `1` AKA `evdev.ecodes.EV_KEY`
                'value': event.value,       # `-1` left or up pressed, `1` right or down pressed, `0` either released
            }
        """
        _dpad = self['dpad'][event.code]

        _event_data = {
            'code': event.code,
            'name': _dpad['name'],
            'usec': event.usec,
            'sec': event.sec,
            'time': event.timestamp(),
            'type': event.type,
            'value': event.value,
        }

        _dpad['last_event'] = _event_data
        return _event_data

    def next(self):
        """
        Inheriting classes may need to overwrite or super this method.

        - Called implicitly via `for` loops but maybe called explicitly.
        - `GeneratorExit`/`StopIteration` are an exit signal for loops.

        Each `event_data` iteration may contain the following

            {
                'code': event.code,         # `0` AKA `evdev.ecodes.ABS_X`
                'name': _axis['name'],      # `stick_left_x`
                'usec': event.usec,         # `211142L`
                'sec': event.sec,           # `4267000555L`
                'time': event.timestamp(),  # `4267000555.211142`
                'type': event.type,         # `3` AKA `evdev.ecodes.EV_ABS`
                'value': event.value,       # `0` to `255` for generic pads
            }
        """
        try:
            event = self['device'].read_one()
        except IOError as e:
            self.throw(GeneratorExit)
        else:
            if not event:
                pass

            elif event.type != evdev.ecodes.EV_KEY and event.type != evdev.ecodes.EV_ABS:
                pass

            elif event.code in self['buttons'].keys():
                return self['buttons'][event.code]['callback'](event)

            elif event.code in self['axes'].keys():
                return self['axes'][event.code]['callback'](event)

            elif event.code in self['dpad'].keys():
                return self['dpad'][event.code]['callback'](event)

    def throw(self, type = None, traceback = None):
        """
        Halts loops iteration on Python 2 or 3 when called via `.throw(GeneratorExit)`
        """
        raise StopIteration

    # Python version compatibility redirection to `.next()` method
    __next__ = next


if __name__ == '__main__':
    import time

    xjoypad = XJoypad()
    for event_data in xjoypad:
        if event_data:
            print("{name} -> {value}".format(**event_data))

        time.sleep(0.001)
