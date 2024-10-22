# filter_plugins/generate_paths.py
import os.path


def generate_paths(tree, parent=""):
    """
    flattens a nested directory tree of directory names into a list of paths.

    :param tree: Nested dictionary containing the tree to flatten.
    :param parent: The parent directory of the directory tree.
    """
    paths = []
    for key, value in tree.items():
        current_path = os.path.join(parent, key) if parent else key
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    paths.append(os.path.join(current_path, item))
                elif isinstance(item, dict):
                    for subkey, subvalue in item.items():
                        paths.extend(generate_paths({subkey: subvalue}, current_path))
        elif isinstance(value, dict):
            paths.extend(generate_paths(value, current_path))
        else:
            paths.append(current_path)
    return paths


class FilterModule(object):
    def filters(self):
        return {
            'generate_paths': generate_paths
        }
