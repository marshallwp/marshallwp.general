# filter_plugins/generate_paths.py
import grp


def get_grpname(gid):
    """
    Get the name of the group with the supplied gid.  If a string is provided, it searches for the group
    entry by name and returns its name. If the gid or name does not match a group, an error is thrown.

    :param gid: The Group ID to get the name for
    """
    grpname = None
    if gid is None:
        raise ValueError("get_grpname requires 1 argument to be specified.")
    elif isinstance(gid, int):
        grpname = grp.getgrgid(gid).gr_name
    else:
        grpname = grp.getgrnam(gid).gr_name
    return grpname


class FilterModule(object):
    def filters(self):
        return {
            'get_grpname': get_grpname
        }
