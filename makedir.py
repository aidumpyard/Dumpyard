import os

def make_dir_tree(root_dir, tree_structure):
    """
    Create a directory tree starting from the root_dir.

    :param root_dir: The root directory where the tree will be created.
    :param tree_structure: A nested dictionary representing the directory tree structure.
    """
    for dir_name, subdirs in tree_structure.items():
        current_dir = os.path.join(root_dir, dir_name)
        os.makedirs(current_dir, exist_ok=True)
        if isinstance(subdirs, dict):
            make_dir_tree(current_dir, subdirs)

# Example usage
tree = {
    'dir1': {
        'subdir1': {},
        'subdir2': {},
    },
    'dir2': {},
    'dir3': {
        'subdir1': {
            'subsubdir1': {},
        },
    },
}

make_dir_tree('my_root_directory', tree)