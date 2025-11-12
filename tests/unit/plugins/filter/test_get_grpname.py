# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.marshallwp.general.plugins.filter.get_grpname import get_grpname
import pytest


# We use the @pytest.mark.parametrize decorator to parametrize the function
# https://docs.pytest.org/en/latest/how-to/parametrize.html
# Simply put, the first element of each tuple will be passed to
# the test_convert_to_supported function as the test_input argument
# and the second element of each tuple will be passed as
# the expected argument.
# In the function's body, we use the assert statement to check
# if the convert_to_supported function given the test_input,
# returns what we expect.
@pytest.mark.parametrize('gid, expected', [
    (0, 'root'),
    ('root', 'root')
])
def test_outputs_grpname(gid, expected):
    assert get_grpname(gid) == expected


def test_throws_KeyError():
    with pytest.raises(KeyError):
        get_grpname('invalidGroup')
