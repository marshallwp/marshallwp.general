<!--
SPDX-FileCopyrightText: 2026 Industrial Info Resources, Inc. <https://www.industrialinfo.com>
SPDX-FileContributor: William P. Marshall

SPDX-License-Identifier: GPL-3.0-or-later
-->

marshallwp.general java Role
========================

Installs Java from a variety of vendors and variants.  You can do a simple Default OpenJDK install, or you can install Oracle Java, or Oracle GraalVM, or the one from Azul, Microsoft, SAP, etc.  Default settings are to install the headless OpenJDK JRE available in your distro's default repository.

Repository URLs and package names follow each vendor's documented naming pattern and are templated from facts, so they keep working as vendors publish for new distribution releases.  Whether a vendor publishes for a given release is up to the vendor.

Repository-based installs are handled via the `marshallwp.general.deps_mgr` role, while non-repository-based installs are handled through the separate `download-and-install.yml` task file.  Repository-based management is preferred where possible.

Archive-based installs strip the archive's top-level directory, so the JDK lands directly in `java_install_directory` and `{{ java_install_directory }}/bin/java` is a fixed path. Installs made by 1.5.7 or earlier under the old default path, which lacked `java_variant`, are moved to the new path automatically, and the old path is replaced with a symlink.

Requirements
------------
<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

This package depends upon the `marshallwp.general.deps_mgr` role and so shares its requirement for `community.general`.

Role Variables
--------------

| Name | Description | Default |
| ---- | ----------- | ------- |
| java_version | Default Java Version. By default it queries Oracle for the latest LTS version of Java. | |
| java_type | Indicates whether the role should try to install the JRE or JDK. | jre |
| java_use_headless | Headless variants exclude GUI components and are good for terminal-only servers. | true |
| java_vendor | The vendor providing you with Java.  `Default` means your distro's default repositories.  See [Supported Vendors](#supported-vendors-and-variants). | Default |
| java_variant | Some vendors provide multiple versions of Java. This variable lets you specify which to install.  See [Supported Vendors](#supported-vendors-and-variants). | OpenJDK |
| java_install_directory | Install directory for non-repository-based installs. | `/usr/lib/jvm/{{ java_type }}-{{ java_version }}-{{ java_vendor }}-{{ java_variant }}-{{ ansible_facts.architecture }}` |
| java_archive_download_dir | Archive download directory for non-repository-based installs. The archive is kept so later runs can skip the download. | `/var/cache/java` |
| java_update_alternatives | Enable or disable updating alternatives for Java | false |
| java_archive_exts | When not installing from a repository, file extension will determine whether a file is installed via ansible.builtin.package or extracted via ansible.builtin.unarchive.  Files with extensions matching this list will go through the latter process. | `['.bz2','.tbz','.gz','.tgz','.lz','.lzma','.tlz','.xz','.txz','.zst','.tzst']` |

Supported Vendors and Variants
------------------------------

### Package-based Installs

**JRE** and **Headless** say whether `java_type: jre` and `java_use_headless: true` are honored; where they aren't, the JDK (or the non-headless package) is installed instead.

| java_vendor | java_variant | OS families | JRE | Headless |
| ----------- | ------------ | ----------- | --- | -------- |
| Default | OpenJDK | Alpine, Altlinux, Archlinux, Debian, Gentoo[^gentoo-headless], RedHat, Suse | Yes | Yes |
| Default | OpenJDK | FreeBSD, Void | Yes | No |
| Default | OpenJDK | Darwin | No | No |
| Amazon (Corretto) | OpenJDK | Alpine, Debian, RedHat, Suse | Amazon Linux only | Amazon Linux only |
| Azul (Zulu) | OpenJDK | Alpine, Debian, RedHat, Suse | Yes | Yes (except Alpine) |
| Azul (Platform Prime) | Prime, Zing | Debian, RedHat, Suse | No | No |
| Bellsoft (Liberica) | OpenJDK | Alpine, Debian, RedHat, Suse | Yes | Yes |
| Eclipse (Temurin) | OpenJDK | Alpine, Debian, RedHat, Suse | Yes | RedHat only |
| Microsoft | OpenJDK | Debian, Suse | No | No |
| SAP (SapMachine) | OpenJDK | Alpine, Debian, RedHat, Suse | No | No |

[^gentoo-headless]: Gentoo controls headless builds with the `headless-awt` USE flag, which the role doesn't set. Set it yourself (e.g. in `/etc/portage/package.use`) if you want a headless install.

### Archive-based Installs

These always install a JDK, and only on glibc-based Linux.

| java_vendor | java_variant |
| ----------- | ------------ |
| Oracle | GraalVM |
| Oracle | Java |

### Unsupported

- IBM Semeru, Alibaba Dragonwell, GraalVM Community Edition and BellSoft Liberica Native Image Kit don't publish repositories or downloads addressable by major version alone.
- Microsoft OpenJDK packages aren't installed on the RedHat family, whose only Microsoft repository (CentOS 7) isn't maintained for current releases.
- Microsoft Azure Linux uses `tdnf`, which `ansible.builtin.package` doesn't support.

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
      java_version: 25
      java_vendor: Oracle
      java_variant: Java
    # Install Bellsoft OpenJDK
    - role: marshallwp.general.java
      java_version: 25
      java_vendor: Bellsoft
    # Install Amazon Corretto (their OpenJDK Build)
    - role: marshallwp.general.java
      java_version: 25
      java_vendor: Amazon
      java_variant: OpenJDK
    # Install Azul Platform Prime (formerly Zing)
    - role: marshallwp.general.java
      java_version: 25
      java_vendor: Azul
      java_variant: Prime
```

Another way to consume this role would be:

```yaml
- name: Install Java
  hosts: all
  gather_facts: false
  tasks:
    - name: Install Azul Zulu 25
      ansible.builtin.include_role:
        name: marshallwp.general.java
      vars:
        java_version: 25
        java_vendor: Azul
        java_variant: OpenJDK
```
