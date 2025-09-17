# filter_plugins/to_filesize.py

DOCUMENTATION = r'''
    name: to_filesize
    short_description: Convert an integer of bytes into a human readable representation.
    version_added: 1.5.0
    author: William P. Marshall
    description:
        - Convert an integer of bytes into a human readable representation.
        - Supports IEC and SI output.
    options:
        _input:
            description: FileSize as an integer of bits or bytes.
            type: integer
            required: true
        prefer_binary:
            description: If True, prefer binary units (KiB, MiB, etc.). If False, prefer decimal units (KB, MB, etc.).
            type: boolean
            required: false
        in_bits:
            description: If True, the input integer represents Bits instead of Bytes.
            type: boolean
            required: false
'''

RETURN = r'''
    _value:
        description: Human-readable representation of input.
        type: string
'''

from filesizelib import FileSize, StorageUnit
from ansible.module_utils.common.text.converters import to_text


def to_filesize(_input, prefer_binary = False, in_bits = False):
    """
    Convert an integer of bytes into a human readable representation.

    :param _input: an integer of bytes.
    :param prefer_binary: If True, prefer binary units (KiB, MiB, etc.). If False, prefer decimal units (KB, MB, etc.).
    :param in_bits: If True, the input integer represents Bits instead of Bytes.
    """
    size = None
    if _input is None:
        raise ValueError("to_filesize requires an input value.")
    elif in_bits is True:
        size = FileSize(_input, StorageUnit.BITS)
    else:
        size = FileSize(_input, StorageUnit.BYTES)
    return to_text(size.auto_scale(prefer_binary))


class FilterModule(object):
    def filters(self):
        return {
            'to_filesize': to_filesize
        }
