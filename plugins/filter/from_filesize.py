# filter_plugins/from_filesize.py

DOCUMENTATION = r'''
    name: from_filesize
    short_description: Convert a human readable filesize into an integer of bytes or bits.
    version_added: 1.5.0
    author: William P. Marshall
    description:
        - Parse the input string with filesizelib and output the number of bytes or bits as an integer.
    options:
        _input:
            description: Human readable filesize string
            type: string
            required: true
        out_bits:
            description: If True, output as bits; if False, output as bytes.
            type: boolean
            required: false
'''

RETURN = r'''
    _value:
        description: Number of bytes (or bits) the string represented.
        type: integer
        sample: 1000
'''

from filesizelib import FileSize

def from_filesize(_input, out_bits = False):
    """
    Convert a human readable filesize into an integer of bytes.

    :param _input: Human readable filesize string
    :param out_bits: If True, output as bits; if False, output as bytes.
    """
    data = None
    if _input is None:
        raise ValueError("from_filesize requires an input value.")
    else:
        data = FileSize(_input)

    if out_bits is True:
        return int(data.BITS.decimal_value)
    else:
        return int(data.BYTES.decimal_value)


class FilterModule(object):
    def filters(self):
        return {
            'from_filesize': from_filesize
        }
