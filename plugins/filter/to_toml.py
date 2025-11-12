# SPDX-FileCopyrightText: 2025 arillso
# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: MIT
# This code is adapted from https://github.com/arillso/ansible.system/blob/42edd560716685e5fe81b3b07540610588a4bd92/plugins/filter/toml.py

DOCUMENTATION = r"""
    name: to_toml
    short_description: Converts a dictionary into a TOML-formatted string
    version_added: 1.5.0
    author: arillso
    description:
        - Converts a dictionary into a TOML string
    options:
        _input:
            description: A dictionary to convert into a TOML string.
            type: dict
            required: true
"""

RETURN = r"""
    _value:
        description: A TOML string
        type: string
"""

from __future__ import absolute_import, division, print_function

import sys

# pylint: disable=import-error
from ansible.errors import AnsibleFilterError, AnsibleRuntimeError
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.common.text.converters import to_text


# Importing libraries for writing TOML
try:
    import tomli_w as tomlw
except ImportError as exc:
    try:
        # Only available on ansible-core below 2.19
        import ansible.plugins.inventory.toml as tomlw
    except ImportError:
        raise AnsibleRuntimeError(
            'The Python library "tomli-w" is required for writing TOML on ansible-core 2.19+.',
        ) from exc


def to_toml(_input):
    """
    Converts a Python object into a TOML-formatted string.

    :param _input: The Python object to convert.
    :type _input: Mapping
    :return: A string in TOML format.
    :rtype: str
    :raises AnsibleFilterError: If the object cannot be converted or another error occurs.
    """
    if not isinstance(_input, Mapping):
        raise AnsibleFilterError(f"to_toml requires a dict, received: {type(_input).__name__}")
    try:
        return to_text(tomlw.dumps(_input), errors="surrogate_or_strict")
    except Exception as e:
        raise AnsibleFilterError(f"Error generating TOML: {e}") from e


# pylint: disable=R0903
class FilterModule:
    """
    to_toml converts Python objects to TOML strings.
    """

    def filters(self):
        """
        Defines the filters provided by this module.

        :return: A dictionary of filter names to filter functions.
        :rtype: dict
        """
        return {
            "to_toml": to_toml,
        }
