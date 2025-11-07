<!--
SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
SPDX-FileContributor: William P. Marshall

SPDX-License-Identifier: GPL-3.0-or-later
-->

marshallwp.general dirtree Role
========================

Creates a directory tree from a dictionary of dictionaries. Lets you declare such a tree in an intuitive hierarchical manner instead of a flat list of paths.

Requirements
------------
<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

None. All needed ansible modules are in `ansible.builtin`, all python plugins are included in this module, and those plugins depend entirely on builtin python libraries.

Role Variables
--------------

| Name | Description | Default |
| ---- | ----------- | ------- |
| dirtree_root | The root directory the dirtree will be created in | `/` |
| dirtree_owner | The owner of created directories.  Passed directly to `ansible.builtin.file` | `ansible_user_id` |
| dirtree_group | The group of created directories.  Passed directly to `ansible.builtin.file` | `ansible_user_gid` |
| dirtree_mode | The permissions the resulting directories should have. Can be set as octals or in symbolic mode. | |
| dirtree_tree | The nested dictionary defining the directory tree. | |

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Create Directory Tree Under /tmp
  hosts: servers
  roles:
    - role: marshallwp.general.dirtree
      dirtree_root: /tmp
      dirtree_tree:
        dir1:
          subdir_lvl1:
            subdir_lvl2:
              - subdir_lvllast
        dir2:
          subdir1_lvl1:
          subdir2_lvl2:
            subdir_lvllast:
        dir3_lvllast:
```

Another way to consume this role would be:

```yaml
- name: Create Directory Tree Under ~
  hosts: servers
  gather_facts: false
  tasks:
    - name: Trigger invocation of run role
      ansible.builtin.include_role:
        name: marshallwp.general.dirtree
      vars:
        dirtree_root: ~
        dirtree_tree:
          dir1:
            subdir_lvl1:
              subdir_lvl2:
                - subdir_lvllast
          dir2:
            subdir1_lvl1:
            subdir2_lvl2:
              subdir_lvllast:
          dir3_lvllast:
```
