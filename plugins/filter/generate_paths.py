# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = r'''
    name: generate_paths
    short_description: Flattens a nested directory tree of directory names into a list of paths.
    description:
        - Flattens a nested dictionary tree of directories into a list of paths.
        - Then uses those paths with `ansible.builtin.file` to ensure that the entire tree exists.
    version_added: 1.0.0
    author: William P. Marshall
    options:
        tree:
            description: Nested dictionary containing the tree to flatten.
            type: dictionary
            required: true
        parent:
            description: The parent directory of the directory tree.
            type: string
'''

RETURN = r'''
    _value:
        description: a list of directory paths
        type: list
        elements: string
'''

import os.path
from ansible.module_utils.common.text.converters import to_text


def generate_paths(tree, parent=""):
    """
    flattens a nested directory tree of directory names into a list of paths.

    :param tree: Nested dictionary containing the tree to flatten.
    :param parent: The parent directory of the directory tree.
    """
    paths = []
    for key, value in tree.items():
        current_path = os.path.join(parent, key) if parent else key
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    paths.append(to_text(os.path.join(current_path, item)))
                elif isinstance(item, dict):
                    for subkey, subvalue in item.items():
                        paths.extend(generate_paths({subkey: subvalue}, current_path))
        elif isinstance(value, dict):
            paths.extend(generate_paths(value, current_path))
        else:
            paths.append(to_text(current_path))
    return paths


class FilterModule(object):
    def filters(self):
        return {
            'generate_paths': generate_paths
        }
