<!--
SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
SPDX-FileContributor: William P. Marshall

SPDX-License-Identifier: GPL-3.0-or-later
-->

marshallwp.general java Role
========================

Installs Java from a variety of vendors and variants.  You can do a simple Default OpenJDK install, or you can install Oracle Java, or Oracle GraalVM, or the one from Azul, Microsoft, etc.  Default settings are to install the headless OpenJDK JRE available in your distro's default repository.

Repository-based installs are handled via the `marshallwp.general.deps_mgr` role, while non-repository-based installs are handled through the separate `download-and-install.yml` task file.  Repository-based management is preferred where possible.

Requirements
------------
<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

This package depends upon the `marshallwp.general.deps_mgr` role and so shares its requirement for `community.general`.

Role Variables
--------------

| Name | Description | Default |
| ---- | ----------- | ------- |
| java_version | Default Java Version.  Should always be a supported version of java. | 21 |
| java_type | Indicates whether the role should try to install the JRE or JDK. | jre |
| java_use_headless | Headless variants exclude GUI components and are good for terminal-only servers. | true |
| java_vendor | The vendor providing you with Java.  `Default` means your distro's default repositories. | Default |
| java_variant | Some vendors provide multiple versions of Java. This variable lets you specify which to install. | OpenJDK |
| java_install_directory | Install directory for non-repository-based installs. | `/usr/lib/jvm/{{ java_type }}-{{ java_version }}-{{ java_vendor }}-{{ ansible_architecture }}` |
| java_archive_download_dir | Archive download directory for non-repository-based installs. | `/tmp` |
| java_update_alternatives | Enable or disable updating alternatives for Java | false |
| java_archive_exts | When not installing from a repository, file extension will determine whether a file is installed via ansible.builtin.package or extracted via ansible.builtin.unarchive.  Files with extensions matching this list will go through the latter process. | `['.bz2','.tbz','.gz','.tgz','.lz','.lzma','.tlz','.xz','.txz','.zst','.tzst']` |

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

`community.general`

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Install Java
  hosts: all
  roles:
    # Install the the latest LTS of the Default OpenJDK
    - marshallwp.general.java
    # Install Oracle Java (not OpenJDK)
    - role: marshallwp.general.java
      java_version: 21
      java_vendor: Oracle
      java_variant: Java
    # Install Bellsoft OpenJDK
    - role: marshallwp.general.java
      java_version: 21
      java_vendor: Bellsoft
    # Install Amazon Corretto (their OpenJDK Build)
    - role: marshallwp.general.java
      java_version: 21
      java_vendor: Amazon
      java_variant: OpenJDK
```

Another way to consume this role would be:

```yaml
- name: Install Java
  hosts: all
  gather_facts: false
  tasks:
    - name: Install Azul Zulu 21
      ansible.builtin.include_role:
        name: marshallwp.general.java
      vars:
        java_version: 21
        java_vendor: Azul
        java_variant: OpenJDK
```
