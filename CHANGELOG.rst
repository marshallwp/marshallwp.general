===========================================
Marshallwp General Collection Release Notes
===========================================

.. contents:: Topics

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

