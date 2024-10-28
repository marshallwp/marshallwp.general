===========================================
Marshallwp General Collection Release Notes
===========================================

.. contents:: Topics

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

- deps_mgr - Quoted the name of the 'Make Packages' task in packages.yml.

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

