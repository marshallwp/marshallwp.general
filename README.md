<!--
SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
SPDX-FileContributor: William P. Marshall

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Marshallwp General Collection

This repository contains the `marshallwp.general` Ansible Collection.  Everything within this collection is useful in wide-ranging situations and contains minimal external dependencies.  It is intended to be extremely generic and where possible has no platform limitations.  Where platform limitations do exist (such as the `deps_mgr` role), they are made as broad as possible.

<!--start requires_ansible-->
Requires Ansible 2.15 or later
<!--end requires_ansible-->

## External requirements

### Ansible Collections
- `community.general`

### Python Libraries
- `tomli-w` – only if you want to use the `to_toml` filter.
- `tomli` – only if you want to use the `from_toml` filter while running on Python ≤ 3.10.  Python 3.11 and later have built-in support for parsing.

## Included content

<!--start collection content-->
<!--end collection content-->

## Using this collection

```bash
    ansible-galaxy collection install marshallwp.general
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: marshallwp.general
```

To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install marshallwp.general --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax where `X.Y.Z` can be any [available version](https://galaxy.ansible.com/marshallwp/general):

```bash
ansible-galaxy collection install marshallwp.general:==X.Y.Z
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/marshallwp/marshallwp.general/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://github.com/marshallwp/marshallwp.general/blob/main/LICENSES/GPL-3.0-or-later.txt) to see the full text.

Some content was adapted from projects under different, but [GPL-compatible](https://www.gnu.org/licenses/license-list.en.html#GPLCompatibleLicenses), licensing schemes. All such content is marked via the `SPDX-License-Identifier` header or snippet identifier. You may use these specific sections under the license indicated, but the overall project remains GPL-3.0-or-later licensed.

A copy of all licenses used in the project can be found in the [LICENSES](https://github.com/marshallwp/marshallwp.general/blob/main/LICENSES/) directory.

This project attempts to comply with the [REUSE specification](https://reuse.software/spec-3.3/), though I'm still considering how to handle files that are largely scaffolding provided by ansible-creator.
