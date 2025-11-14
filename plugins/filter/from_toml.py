# SPDX-FileCopyrightText: 2025 arillso
# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: MIT
# This code is adapted from https://github.com/arillso/ansible.system/blob/42edd560716685e5fe81b3b07540610588a4bd92/plugins/filter/toml.py

from __future__ import absolute_import, division, print_function

import sys

# pylint: disable=import-error
from ansible.errors import AnsibleFilterError, AnsibleRuntimeError


DOCUMENTATION = r"""
    name: from_toml
    short_description: Converts a TOML-formatted string into a Python object.
    version_added: 1.5.0
    author: arillso
    description:
        - Converts a TOML string into a Python Object
    options:
        _input:
            description: A TOML string
            type: string
            required: true
"""

RETURN = r"""
    _value:
        description: The parsed output as a dictionary
        type: dict
"""

# Importing libraries for reading
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError as exc:
        raise AnsibleRuntimeError(
            'The Python library "tomli" is required for reading TOML in Python 3.10 and below.',
        ) from exc


def from_toml(_input):
    """
    Converts a TOML-formatted string into a Python object.

    :param _input: The string to convert.
    :type _input: str
    :return: The Python object generated from the TOML string.
    :rtype: dict
    :raises AnsibleFilterError: If the input string is not a valid TOML string or another
        error occurs.
    """
    if not isinstance(_input, str):
        raise AnsibleFilterError(
            f"from_toml requires a string, received: {type(_input).__name__}",
        )
    try:
        return tomllib.loads(_input)
    except Exception as e:
        raise AnsibleFilterError(f"Error parsing TOML: {e}") from e


# pylint: disable=R0903
class FilterModule:
    """
    from_toml sonverts TOML strings to Python objects.
    """

    def filters(self):
        """
        Defines the filters provided by this module.

        :return: A dictionary of filter names to filter functions.
        :rtype: dict
        """
        return {
            "from_toml": from_toml,
        }
