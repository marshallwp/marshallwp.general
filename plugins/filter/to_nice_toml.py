# SPDX-FileCopyrightText: 2025 arillso
# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: MIT
# This code is adapted from https://github.com/arillso/ansible.system/blob/42edd560716685e5fe81b3b07540610588a4bd92/plugins/filter/toml.py

from __future__ import absolute_import, division, print_function

from datetime import datetime

from ansible.module_utils.common.text.converters import to_text


DOCUMENTATION = r"""
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
"""

RETURN = r"""
    _value:
        description: A TOML string
        type: string
"""


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

    return to_text(recurse(_input))


# pylint: disable=R0903
class FilterModule:
    """
    to_nice_toml converts Python objects to nicely formatted TOML strings.
    """

    def filters(self):
        """
        Defines the filters provided by this module.

        :return: A dictionary of filter names to filter functions.
        :rtype: dict
        """
        return {
            "to_nice_toml": to_nice_toml,
        }
