# SPDX-FileCopyrightText: 2025 arillso
# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: MIT

# This code is derived from https://github.com/arillso/ansible.system/blob/42edd560716685e5fe81b3b07540610588a4bd92/plugins/filter/toml.py

"""
Ansible Filter Plugin for TOML conversion.

This module provides filters for converting between TOML strings and Python objects,
with support for Python versions before and after 3.11.
"""

from __future__ import absolute_import, division, print_function

import sys
from datetime import datetime

# pylint: disable=import-error
from ansible.errors import AnsibleFilterError, AnsibleRuntimeError
from ansible.module_utils._text import to_text
from ansible.module_utils.common._collections_compat import Mapping

# Importing libraries for reading and writing TOML
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError as exc:
        raise AnsibleRuntimeError(
            'The Python library "tomli" is required for reading TOML.'
        ) from exc

try:
    import tomli_w as tomlw
except ImportError as exc:
    try:
        # Only available on ansible-core below 2.19
        import ansible.plugins.inventory.toml as tomlw
    except ImportError:
        raise AnsibleRuntimeError(
            'The Python library "tomli-w" is required for writing TOML on ansible-core 2.19+.'
        ) from exc


DOCUMENTATION = r'''
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
'''

RETURN = r'''
    _value:
        description: The parsed output as a dictionary
        type: dict
'''


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
            f"from_toml requires a string, received: {type(_input).__name__}"
        )
    try:
        return tomllib.loads(_input)
        # return json.dumps(python_object, default=datetime_converter)
    except Exception as e:
        raise AnsibleFilterError(f"Error parsing TOML: {e}") from e


DOCUMENTATION = r'''
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
'''

RETURN = r'''
    _value:
        description: A TOML string
        type: string
'''


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
        raise AnsibleFilterError(
            f"to_toml requires a dict, received: {type(_input).__name__}"
        )
    try:
        return to_text(tomlw.dumps(_input), errors="surrogate_or_strict")
    except Exception as e:
        raise AnsibleFilterError(f"Error generating TOML: {e}") from e


DOCUMENTATION = r'''
    name: to_nice_toml
    short_description: Converts a dictionary into a nice TOML-formatted string
    version_added: 1.5.0
    author: arillso
    description:
        - This function formats a Python dictionary into a TOML string, taking special care to handle
        - nested dictionaries and arrays of dictionaries. It ensures proper indentation and formatting
        - to produce a readable TOML representation of the input dictionary.
    options:
        _input:
            description: A dictionary to convert into a TOML string.
            type: dict
            required: true
'''

RETURN = r'''
    _value:
        description: A TOML string
        type: string
'''


def to_nice_toml(_input):
    """
    Convert a Python dictionary to a nicely formatted TOML string.

    This function formats a Python dictionary into a TOML string, taking special care to handle
    nested dictionaries and arrays of dictionaries. It ensures proper indentation and formatting
    to produce a readable TOML representation of the input dictionary.

    :param _input: The Python dictionary to convert.
    :type _input: dict
    :return: A nicely formatted TOML string representing the input dictionary.
    :rtype: str
    """

    def format_toml_value(value):
        """
        Format a Python value into a TOML-friendly string representation, ensuring
        date-time values are correctly formatted as YYYY-MM-DDTHH:MM:SSZ.
        """
        if isinstance(value, str):
            # Check if the value is a date-time string in ISO format.
            try:
                # Attempt to parse the string as a datetime object.
                parsed_datetime = datetime.fromisoformat(value.rstrip("Z"))
                # Reformat to the specific desired format with 'Z'.
                return parsed_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                # If parsing fails, return the value as a regular string.
                return f'"{value}"'
        elif isinstance(value, datetime):
            # Format datetime objects directly.
            return value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            # Ensure that each item in the list is correctly formatted.
            return "[" + ", ".join(map(format_toml_value, value)) + "]"
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def recurse(_input, indent=0, parent_key=""):
        """
        Recursively traverses the data structure, formatting it into a TOML string.

        This helper function handles the recursion needed for nested dictionaries
        and arrays of dictionaries,ensuring proper TOML structure and indentation.
        """
        toml_str = ""
        for key, value in _input.items():
            # Construct the full key path for nested dictionaries
            full_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                # For nested dictionaries, add a section header
                if indent <= 0:  # Not for the top-level
                    toml_str += "\n"
                prefixed_key = full_key if parent_key else key
                toml_str += "  " * indent + f"[{prefixed_key}]\n"
                toml_str += recurse(value, indent + 1, full_key)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # For arrays of dictionaries, add array of tables header
                for item in value:
                    toml_str += "\n" + "  " * indent + f"[[{full_key}]]\n"
                    toml_str += recurse(item, indent + 1, full_key)
            else:
                # Simple key-value pairs
                toml_str += "  " * indent + f"{key} = {format_toml_value(value)}\n"
        return toml_str

    return recurse(_input)


# pylint: disable=R0903
class FilterModule:
    """
    Ansible Filter Module for converting between TOML and Python objects with improved formatting.

    Provides three filters:
    - from_toml: Converts TOML strings to Python objects.
    - to_toml: Converts Python objects to TOML strings.
    - to_nice_toml: Converts Python objects to nicely formatted TOML strings.
    """

    def filters(self):
        """
        Defines the filters provided by this module.

        :return: A dictionary of filter names to filter functions.
        :rtype: dict
        """
        return {
            "to_toml": to_toml,
            "to_nice_toml": to_nice_toml,
            "from_toml": from_toml,
        }
