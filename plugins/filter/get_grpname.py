# filter_plugins/generate_paths.py

DOCUMENTATION = r'''
    name: get_grpname
    short_description: Match the input name or GID to a real group and return its name.
    version_added: 1.0.0
    author: William P. Marshall
    description:
        - Get the name of the group with the supplied gid or name. If a string is provided, it searches for the group entry by name and returns its name.
        - If the gid or name does not match a group, an error is thrown.
    options:
        _input:
            description: A group name or GID to search for.
            type: string
            required: true
'''

RETURN = r'''
    _value:
        description: A valid group name.
        type: string
        sample: mygroup
'''

import grp
from ansible.module_utils.common.text.converters import to_text


def get_grpname(_input):
    """
    Get the name of the group with the supplied gid or name. If a string is provided, it searches
    for the group entry by name and returns its name. If the gid or name does not match a group,
    an error is thrown.

    :param _input: The Group ID or Name to search for.
    """
    grpname = None
    if _input is None:
        raise ValueError("get_grpname requires 1 argument to be specified.")
    elif isinstance(_input, int):
        grpname = grp.getgrgid(_input).gr_name
    else:
        grpname = grp.getgrnam(_input).gr_name
    return to_text(grpname)


class FilterModule(object):
    def filters(self):
        return {
            'get_grpname': get_grpname
        }
