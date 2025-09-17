from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.marshallwp.general.plugins.filter.from_filesize import from_filesize
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
@pytest.mark.parametrize('filesize, isbits, expected', [
    ('10 MiB', False, 10485760),
    ('24 KB', True, 192000),
    ('24 KB', False, 24000)
])
def test_outputs_filesize(filesize, isbits, expected):
    assert from_filesize(filesize, isbits) == expected


@pytest.mark.parametrize('sample, expected', [
    ('invalid_value', ValueError),
    (None, ValueError)
])
def test_throws_KeyError(sample, expected):
    with pytest.raises(expected):
        from_filesize(sample)
