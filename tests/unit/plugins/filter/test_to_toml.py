# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: GPL-3.0-or-later


from __future__ import absolute_import, division, print_function


__metaclass__ = type

import pytest

from ansible.errors import AnsibleFilterError

from ansible_collections.marshallwp.general.plugins.filter.to_toml import to_toml


# We use the @pytest.mark.parametrize decorator to parametrize the function
# https://docs.pytest.org/en/latest/how-to/parametrize.html
# Simply put, the first element of each tuple will be passed to
# the test_convert_to_supported function as the test_input argument
# and the second element of each tuple will be passed as
# the expected argument.
# In the function's body, we use the assert statement to check
# if the convert_to_supported function given the test_input,
# returns what we expect.
@pytest.mark.parametrize(
    "sample, expected",
    [
        (
            {"table": {"nested": {}, "val3": 3}, "val2": 2, "val1": 1},
            """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
""",
        ),
    ],
)
def test_outputs_to_toml(sample, expected):
    assert to_toml(sample) == expected


def test_to_toml_throws_AnsibleFilterError():
    with pytest.raises(AnsibleFilterError):
        to_toml("string")
