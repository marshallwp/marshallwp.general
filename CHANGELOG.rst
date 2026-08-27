.. SPDX-FileCopyrightText: 2026 Industrial Info Resources, Inc.
.. SPDX-FileContributor: William P. Marshall
..
.. SPDX-License-Identifier: GPL-3.0-or-later

===========================================
Marshallwp General Collection Release Notes
===========================================

.. contents:: Topics

v1.5.6
======

Release Summary
---------------

Fix a deps_mgr bug where conditional package entries could prevent installation of the other packages in the list.

Bugfixes
--------

- deps_mgr - ``omit`` is now filtered out of package lists. Previously, a conditional entry like ``ternary('pkg', omit)`` left a placeholder string in the list, and installation of the entire list failed. This prevented acme_sh from installing its dependencies (such as ``bind-utils``) on some hosts.

v1.5.5
======

Release Summary
---------------

Fix several variable-naming and templating bugs left over from the migration to ``ansible_facts``, and correct the java role's update-alternatives tasks.

Minor Changes
-------------

- Continued migrating remaining magic variables (`ansible_hostname`, `ansible_distribution_release`, `ansible_architecture`, `ansible_distribution`, `ansible_system`) to their `ansible_facts` equivalents in the `acme_sh`, `deps_mgr`, and `java` roles and tests.

Bugfixes
--------

- acme_sh - Fixed a variable name mismatch (`acme_sh_deps_by_family` renamed to `acme_sh_dependencies`) that prevented the role from installing its required dependencies.
- acme_sh - Corrected a typo (`regexp` to `regex`) in the Jinja test used to detect nsupdate-based DNS challenges, which previously caused a templating error.
- acme_sh - Corrected the README, which documented the old `acme_sh_account_keyfile` and `acme_sh_prehook` variable names instead of the current `acme_sh_account_key_file` and `acme_sh_pre_hook`.
- dirtree - The role now honors the documented `dirtree_owner` variable. It previously referenced an undocumented `dirtree_user` variable, so setting `dirtree_owner` had no effect.
- java - Fixed the update-alternatives tasks, which failed because the `family` parameter was being used incorrectly. They now use the `path`/`link` parameters and point at the correct `/usr/lib/jvm` and `/usr/bin/java` locations.

Documentation Changes
---------------------

- Updated SPDX copyright years to 2026 and removed a leftover `changelogs/.plugin-cache.yaml` reference from `galaxy.yml`.

v1.5.4
======

Release Summary
---------------

Resolve ansible-lint findings by migrating magic variables to ``ansible_facts`` and remove the antsibull-changelog integration.

Breaking Changes
-----------------

- Removed the antsibull-changelog integration (the `changelogs/` directory and its CI workflow job), as it is no longer compatible with the ansible-dev-container. Release notes are now maintained directly in this file.

Minor Changes
-------------

- Migrated magic variables (`ansible_user_id`, `ansible_user_gid`, `ansible_architecture`) to their `ansible_facts` equivalents in the `acme_sh`, `deps_mgr`, `dirtree`, and `java` roles to resolve ansible-lint warnings.

v1.5.3
======

Release Summary
---------------

fixes an issue preventing the acme_sh role from updating deployment commands and allows the from_toml filter to work in more situations.

Minor Changes
-------------

- The from_toml filter now supports using ansible's built-in toml library in ansible-core 2.18 and below.

Bugfixes
--------

- Fix #29 by removing the erronious OR command from line 16 of the update_cmds.yml file.
- Rename "choice" properties to "choices" in argument_specs to make them compliant with specifications.

v1.5.2
======

Release Summary
---------------

Update testing to make Python 3.10 happy and improve java documentation, spec, and default values.

Major Changes
-------------

- The `java` role now queries `Public APIs for Oracle Java Releases <https://docs.oracle.com/en-us/iaas/jms/doc/public-api-oracle-java-releases.html>`_ for the latest LTS version of Java available. This should help reduce the number of updates this role needs that default up-to-date.

Minor Changes
-------------

- Requirements files now include an explicit tomli version.

v1.5.1
======

Release Summary
---------------

Split the TOML filters into multiple files to improve documentation and reduce required dependencies for those interested in using only a subset of the filters.

Minor Changes
-------------

- devcontainer - pre-commit is now installed upon first start of the devcontainer.  This ensures it is enforced without further user configuration.
- pre-commit - rewrote the pre-commit configuration file from scratch so it is no-longer based on RedHat work.

Documentation Changes
---------------------

- README - Added Ansible Galaxy download count and link

v1.5.0
======

Release Summary
---------------

Add filters for converting to and from TOML.

Removed Features (previously deprecated)
----------------------------------------

- deps_mgr - use of the `dependencies` alias for `deps_mgr_list` has been removed due to lack of support in Ansible's Argument Specification.

Documentation Changes
---------------------

- Implement REUSE specification for licensing information.

New Plugins
-----------

Filter
~~~~~~

- from_toml - Converts a TOML-formatted string into a Python object.
- to_nice_toml - Converts a dictionary into a nice TOML-formatted string
- to_toml - Converts a dictionary into a TOML-formatted string

v1.4.3
======

Release Summary
---------------

Add support for installing Microsoft OpenJDK on Suse distributions. Add Ansible argument specs to all roles. Explicitly made deps_mgr package and replsitory management tasks elevated.

Major Changes
-------------

- deps_mgr - explicitly specificed that tasks related to package installation or repository management should be elevated.

Minor Changes
-------------

- Add argument spec to acme_sh role.
- Add argument spec to deps_mgr role.
- Add argument spec to dirtree role.
- Add argument spec to java role.
- Add support for installing Microsoft OpenJDK for Suse distributions.

v1.4.2
======

Release Summary
---------------

Eliminates open-ended copy operations and makes ansible code-checking happy.

Minor Changes
-------------

- dns_nsupdates.sh was altered to make shellcheck and ansible shebang sanity test happy.

Security Fixes
--------------

- acme_sh will no longer copy keys (of which there are none) from the role's files/keys directory to the destination.

v1.4.1
======

Release Summary
---------------

Fixes a bug in the acme_sh role that causes it to fail when specifying cron as the scheduler.

Bugfixes
--------

- `acme_sh` role would fail when you used cron as the scheduler. This was caused by a lack of error handling for systemd_service ansible roles, which produced errors about systemd services not existing.

v1.4.0
======

Release Summary
---------------

Add a role to manage acme.sh and fix a few documentation issues.

New Roles
---------

- acme_sh - Manage acme.sh, a lightweight certificate managemenent tool.

v1.3.3
======

Release Summary
---------------

In deps_mgr, fix looping issues with the packages handler and default value issues with the repository_types handlers.

Bugfixes
--------

- deps_mgr - flatten the query results used to loop Manage Packages by Desired State in packages.yml.  This will allow us to use query to ensure looping, but flatten the looped value down to one list.
- deps_mgr - repository_types handlers now use `default(omit)` when a parameter is not specified.  Fixes issues related to type casting.

v1.3.2
======

Release Summary
---------------

Fixes documentation by removing duplicates, clarifying examples, and rectifying typos.

Documentation Changes
---------------------

- docs(deps_mgr) - clarify examples and how the alpine repo_type is managed.
- docs(java) - fix typo in vars/main.yml comments.
- docs(java) - remove duplicate text from parameter description.

v1.3.1
======

Release Summary
---------------

fixed a bug that broke archive-based installs of java.

Minor Changes
-------------

- can now skip changing alternatives after installing an archived copy of Java.

Bugfixes
--------

- Missing destination directory creation step in archive extraction.
- The `java_archive_path` variable was composed using the invalid `java_archive_installers` variable instead of the `java_archives` variable.
- Typo, `ansible.builtin.splitent` was used instead of `ansible.builtin.splitext`.
- Unarchive task required remote_src = true to work.

v1.3.0
======

Release Summary
---------------

Added a new Java role and made minor enhancements to deps_mgr.

Minor Changes
-------------

- deps_mgr - alpine repositories now support copying the public key from the controller instead of downloading from a URL.
- deps_mgr - will now gather required facts if they are missing. This allows the role to work if the playbook has``gather_facts: false`` or an incompatible ``gather_subset`` setting.

Documentation Changes
---------------------

- deps_mgr - updated the README.md to fix spelling and formatting errors.

v1.2.0
======

Release Summary
---------------

deps_mgr - Reduced duplicative labels, fixed issues with repository name, added an option to change the default package state, and added integration tests.

Minor Changes
-------------

- deps_mgr - added the new variable `deps_mgr_package_default_state`, which allows users to set the default state for simple packages.

Bugfixes
--------

- deps_mgr - all repository management types now require `name` and ensure it is mapped to a parameter. i.e., the previously documented behavior is now enforced.

v1.1.0
======

Release Summary
---------------

Expanded the number of supported package managers and organized steps for using each one into its own file.

Minor Changes
-------------

- collection - new requirement that community.general be version 8.2.0 or later to support community.general.dnf_conf_manager.
- deps_mgr - added support for apt, apt-repo, copr, and sorcery repositories/grimoires.
- deps_mgr - split repository module code into separate files for each type.  Moved repo var generation to the repositories.yml file.

Documentation Changes
---------------------

- deps_mgr - Added a breakdown of `dep_mgr_list` syntax.
- deps_mgr - Added a list of common repository parameters.
- deps_mgr - Added documentation for the new repository types.

v1.0.3
======

Release Summary
---------------

Allow the user to specify how different levels of the deps_mgr_list are merged.

Minor Changes
-------------

- deps_mgr - You can now specify whether to use the `lowest_only` or `precision` merge methods for packages and repositories.

Bugfixes
--------

- deps_mgr - Quoted the name of the 'Make Packages' task in packages.yml so the state variable value is included.

v1.0.2
======

Release Summary
---------------

Fix package installation issues with custom state values.

Bugfixes
--------

- deps_mgr - Quoted and bracketed the "state" variable.  This prevents unexpected failures due to custom states.

v1.0.1
======

Release Summary
---------------

Update documentation collection-wide and make minor bugfixes to plugins.

Bugfixes
--------

- Plugins - All output strings are now run through the included to_text function to ensure proper encoding.
  See: https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#string-encoding

Documentation Changes
---------------------

- LICENSE - corrected licensing to match reality.
- Plugins - Added documentation to all plugins.
- READMEs - Added parameter definitions, expanded on dependency usage, and eliminated leftover templating cruft.

v1.0.0
======
