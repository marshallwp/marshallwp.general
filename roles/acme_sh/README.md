marshallwp.general acme_sh Role
========================

Installs/Uninstalls and (re)configures acme.sh, custom dnsapi extensions, and scheduled runs of the same.  Acme.sh is "a pure Unix shell script implementing ACME client protocol" for certificate management. It requires minimal dependencies and is compatible with bash, dash, and sh.

## Minimal Dependencies
Using this role will install the following packages on the target:

| name                                 | install condition                      |
| ------------------------------------ | -------------------------------------- |
| **socat**                            | always                                 |
| **openssl**                          | always                                 |
| cron/cronnie/mcron/vixie-cron        | `acme_sh_scheduler == 'cron'`    |
| bind-utils/bind-tools/bind9-dnsutils | `acme_sh_mode == 'dns' and acme_sh_mode_value is regexp('dns_nsupdates?')` |
| wget                                 | neither `wget` nor `curl` is installed |

Requirements
------------
<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

None. All needed ansible modules are in `ansible.builtin`.

Role Variables
--------------

| Name | Description | Default |
| ---- | ----------- | ------- |
| acme_sh_enabled | If set to false, acme.sh will be uninstalled | `true` |
| acme_sh_user | The user that will run and own the output of acme.sh | `root` |
| acme_sh_group | The group that will run and own the output of acme.sh | `root` |
| acme_sh_home | The directory into which acme.sh will be installed and in which configuration files will be stored | `/root/acme` |
| acme_sh_scheduler | The scheduler used to run acme.sh on a schedule. Can be `cron`, `systemd`, or `none` | `cron` |
| acme_sh_auto_update | Whether acme.sh should check for and install updates during scheduled jobs. | `true` |
| acme_sh_tls_cert_file | Destination filepath of the TLS Public Certificate | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/public.crt"` |
| acme_sh_tls_key_file | Destination filepath of the TLS Private Key | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/private.key"` |
| acme_sh_tls_fullchain_file | Destination filepath of the TLS Fullchain Public Certificate | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/public-fullchain.crt"` |
| acme_sh_domain | The domain you want to get a certificate for. | `ansible_facts['nodename']` |
| acme_sh_mode | The mode to use when performing ACME challenges. Can be `dns`,`standalone`, or `alpn` | `dns` |
| acme_sh_mode_value | Some modes (like `dns`) take an input value. Use this to pass it. | `dns_nsupdates` |
| acme_sh_dns_zone | **MANDATORY** The DNS zone used during certificate renewals. | |
| acme_sh_dns_sleep | Time in seconds to wait for all TXT records to propagate in dnsapi mode.  By default acme.sh polls dns status by DOH. | |
| acme_sh_listening_port | The port acme_sh should listen on when using `standalone` or `alpn` modes. | |
| acme_sh_env_variables | A dictionary of environment variables to be set during acme.sh operations.  Primarily for dnsapi extensions. | |
| acme_sh_server | Sets the [`--server`](https://github.com/acmesh-official/acme.sh/wiki/Server) parameter. | `letsencrypt_test` |
| acme_sh_account_email | **MANDATORY** The email of the account to request a certificate under. | |
| acme_sh_account_keyfile | **MANDATORY** File containing your account key for authentication with the ACME server | `"{{ acme_sh_home }}/ca_account.key"` |
| acme_sh_keylength | Specifies the domain key length: 2048, 3072, 4096, 8192 or ec-256, ec-384, ec-521. | `ec-384` |
| acme_sh_reloadcmd | Command run after newly renewed certificates are installed | |
| acme_sh_prehook | Pre hook that happens before attempting to issue a certificate | |
| acme_sh_post_hook | Post hook that happens after attempting to issue a certificate | |
| acme_sh_renew_hook | Renew hook that is called when certs are *successfully* renewed | |
| acme_sh_run_hook_setup | Setup the hooks and reloadcmd. Useful when the command executed by the hook won't work without the certificates existing first. | `true` |

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Invoke acme_sh
  hosts: servers
  roles:
    - marshallwp.general.acme_sh
```

If you need to run acme.sh to generate the certificates before creating the program you want it to reload or hook into during certificate renewal, you can setup the hooks separately like so:

```yaml
- name: Create Directory Tree Under ~
  hosts: servers
  gather_facts: false
  roles:
    - name: marshallwp.general.acme_sh
      acme_sh_run_hook_setup: false
    - nginx
  tasks:
    - name: Update the acme.sh hooks and reloadcmd
      ansible.builtin.include_role:
        name: marshallwp.general.acme_sh
        tasks_from: update_cmds.yml
      vars:
        acme_sh_run_hook_setup: true
```
