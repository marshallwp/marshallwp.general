marshallwp.general deps_mgr Role
========================

Manages OS packages and repositories at the os_family, distribution, and/or distribution_major_version level.  Repository management occurs first to ensure package management succeeds.  While package management commands are performed using the generic `ansible.builtin.package` module, repository management is performed by the command associated with the `method` specified for each repository entry.  As such, repository management is unfortunately platform-specific.

All package management programs supported by `ansible.builtin.package` can be used for package management.  See the definition for the `PKG_MGRS` variable on [pkg_mgr.py](https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/facts/system/pkg_mgr.py).

Repository management is currently only supported by the following:

| repo_type | Implementing Module |
| --------- | ------------------- |
| deb822 | [`ansible.builtin.deb822_repository`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/deb822_repository_module.html) |
| dnf-config | [`community.general.dnf_config_manager`](https://docs.ansible.com/ansible/latest/collections/community/general/dnf_config_manager_module.html) |
| homebrew | [`community.general.homebrew_tap`](https://docs.ansible.com/ansible/latest/collections/community/general/homebrew_tap_module.html) |
| pkg5 | [`community.general.pkg5_publisher`](https://docs.ansible.com/ansible/latest/collections/community/general/pkg5_publisher_module.html) |
| yum | [`ansible.builtin.yum_repository`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_repository_module.html) |
| zypper | [`community.general.zypper_repository`](https://docs.ansible.com/ansible/latest/collections/community/general/zypper_repository_module.html) |

Requirements
------------

Requires the `community.general` collection for DNF Config, Homebrew, Pkg5, and Zypper repository management.  `community.general.lists_mergeby` is also used by the package manager, where it merges lists by precedence.

Role Variables
--------------

| Name | Alias | Description | Default |
| ---- | ----- | ----------- | ------- |
| deps_mgr_package_merge_method | | Merge method to use when choosing what packages to manage and how. | precedence |
| deps_mgr_repo_merge_method | | Merge method to use when choosing what repositories to manage and how. | lowest_only |
| deps_mgr_list | dependencies | Hierarchical dictionary of packages and repositories to be configured at the os family, distribution, and major version levels. |

### Merge Methods
If you have packages or repositories specified at multiple levels of the `deps_mgr_list`, the merge method determines how ansible chooses entries to use.  It is set for packages and repositories via the `deps_mgr_package_merge_method` and `deps_mgr_repo_merge_method` variables respectively. Currently we support the following methods:

| Method | Description |
| ------ | ----------- |
| lowest_only | The simplest method, it gets items from the most precise matching list and ignores all the others. |
| precedence | Combine lists with precidence ordered from most precise to least. Higher-level items will be included, but can be overridden by lower level ones. |


Dependencies
------------

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

`community.general`

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
# Example for Installing Postgres 16 with packages required for configuration via community.general.postgres.
- name: Install Postgres 16
  hosts: servers
  roles:
    - role: marshallwp.general.deps_mgr
      dependencies:
        Alpine:
          packages:
            - py3-psycopg
            - "postgresql{{ postgresql_version | default(16) }}"
        Debian:
          repositories:
            - repo_type: deb822
              name: pgdg
              uris: https://apt.postgresql.org/pub/repos/apt
              suites:
                - "{{ ansible_facts['ansible_lsb']['codename'] | default('invalid') }}-pgdg"
                - 'main'
              signed_by: https://www.postgresql.org/media/keys/ACCC4CF8.asc
          packages:
            - python3-psycopg2
            - "postgresql-{{ postgresql_version | default(16) }}"
        RedHat:
          AlmaLinux:
            repositories:
              - repo_type: dnf-config
                name: appstream
          OracleLinux:
            repositories:
              - repo_type: dnf-config
                name: "ol{{ ansible_facts['distribution_major_version'] }}_appstream"
          RedHat:
            repositories:
              - repo_type: dnf-config
                name: "rhel-{{ ansible_facts['distribution_major_version'] }}-for-{{ ansible_architecture }}-appstream-rpms"
          Rocky:
            repositories:
              - repo_type: dnf-config
                name: appstream
          packages:
            - python-psycopg2
            - "@postgresql:{{ postgresql_version | default(16) }}/server"
        Suse:
          packages:
            - python3-psycopg2
            - "postgresql{{ postgresql_version | default(16) }}-server"
```

Another way to consume this role would be:

```yaml
- name: Initialize the run role from marshallwp.general
  hosts: servers
  gather_facts: false
  tasks:
    - name: Trigger invocation of deps_mgr role
      ansible.builtin.include_role:
        name: marshallwp.general.deps_mgr
      vars:
        deps_mgr_list:
          Alpine:
            packages:
              - py3-psycopg
              - "postgresql{{ postgresql_version | default(16) }}"
```
