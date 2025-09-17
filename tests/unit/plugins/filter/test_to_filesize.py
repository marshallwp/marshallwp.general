from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.marshallwp.general.plugins.filter.to_filesize import to_filesize
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
@pytest.mark.parametrize('filesize, prefer_binary, expected', [
    (1500000000, False, '1.5 GB'),
    (1610612736, True, '1.5 GiB'),
    (10561536, True, '10.072265625 MiB')
])
def test_outputs_filesize(filesize, prefer_binary, expected):
    assert to_filesize(filesize, prefer_binary).casefold() == expected.casefold()


@pytest.mark.parametrize('sample, expected', [
    ('invalid_value', ValueError),
    (None, ValueError)
])
def test_throws_KeyError(sample, expected):
    with pytest.raises(expected):
        to_filesize(sample)
