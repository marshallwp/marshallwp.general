.. SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
.. SPDX-FileContributor: William P. Marshall
..
.. SPDX-License-Identifier: GPL-3.0-or-later

===========================================
Marshallwp General Collection Release Notes
===========================================

.. contents:: Topics

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

- acme_sh - A role to install/update/remove, configure, and schedule acme.sh. acme.sh is a certificate manager written purely in Shell and thus has minimal dependencies (wget or curl). It is highly extensible and works on just about anything.

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

