# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.marshallwp.general.plugins.filter.generate_paths import generate_paths
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
@pytest.mark.parametrize('tree, parent, expected', [
    (dict(dir1=dict(dir1_1=None)), None, ['dir1/dir1_1']),
    (dict(dir1=['dir1_1']), None, ['dir1/dir1_1']),
    (dict(dir1=dict(dir1_1=dict(dir1_1_1=None)),
          dir2=dict(dir2_1=None, dir2_2=None)),
        '/',
        ['/dir1/dir1_1/dir1_1_1',
         '/dir2/dir2_1',
         '/dir2/dir2_2']
     ),
    (dict(dir1=None), '/test', ['/test/dir1'])
])
def test_path_generation(tree, parent, expected):
    assert generate_paths(tree, parent) == expected
