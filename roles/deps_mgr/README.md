marshallwp.general deps_mgr Role
========================

Manages OS packages and repositories at the os_family, distribution, and/or distribution_major_version level.  Repository management occurs first to ensure package management succeeds.  While package management commands are performed using the generic `ansible.builtin.package` module, repository management is performed by the command associated with the `method` specified for each repository entry.  As such, repository management is unfortunately platform-specific.

Requirements
------------

Requires the `community.general` collection for DNF Config, Homebrew, Pkg5, and Zypper repository management.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

<!-- A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

community.general

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
          repositories:
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
          repositories:
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
            repositories:
            packages:
              - py3-psycopg
              - "postgresql{{ postgresql_version | default(16) }}"
```

License
-------

# TO-DO: Update the license to the one you want to use (delete this line after setting the license)
BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
