marshallwp.general acme_sh Role
========================

Installs/Uninstalls and (re)configures acme.sh, custom dnsapi extensions, and scheduled runs of the same.  Acme.sh is "a pure Unix shell script implementing ACME client protocol" for certificate management. It requires no dependencies and is compatible with bash, dash, and sh.

Requirements
------------
<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

None. All needed ansible modules are in `ansible.builtin`.

Role Variables
--------------

| Name | Description | Default |
| ---- | ----------- | ------- |
| acme_sh_enabled | If set to false, acme.sh will be uninstalled | `true` |
| acme_sh_user | The user that will run and own the output of acme.sh | `ansible_user_id` |
| acme_sh_group | The group that will run and own the output of acme.sh | `ansible_user_gid` |
| acme_sh_home | The directory into which acme.sh will be instaled and in which configuration files will be stored | `~/acme` |
| acme_sh_scheduler | The scheduler used to run acme.sh on a schedule. Can be `cron`, `systemd`, or `none` | `cron` |
| acme_sh_auto_update | If true, acme.sh will check for and install updates during scheduled jobs. | `true` |
| acme_sh_tls_cert_file | Destination filepath of the TLS Public Certificate | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/public.crt"` |
| acme_sh_tls_key_file | Destination filepath of the TLS Private Key | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/private.key"` |
| acme_sh_tls_fullchain_file | Destination filepath of the TLS Fullchain Public Certificate | `"{{ acme_sh_home }}/{{ ansible_facts['nodename'] }}/public-fullchain.crt"` |
| acme_sh_domain | | `ansible_facts['nodename']` |
| acme_sh_mode | The mode to use when performing ACME challenges. Can be `dns`,`standalone`, or `alpn` | `dns` |
| acme_sh_mode_value | Some modes (like `dns`) take an input value. Use this to pass it. | `dns_nsupdates` |
| acme_sh_dns_zone | **MANDATORY** The DNS zone used during certificate renewals. | |
| acme_sh_dns_sleep | Time in seconds to wait for all TXT records to propegate in dnsapi mode.  By default acme.sh polls dns status by DOH. | |
| acme_sh_listening_port | The port acme_sh should listen on when using `standalone` or `alpn` modes. | |
| acme_sh_env_variables | A dictionary of environment variables to be set during acme.sh operations.  Primarily for dnsapi extensions. | |
| acme_sh_server | Sets the [`--server`](https://github.com/acmesh-official/acme.sh/wiki/Server) parameter. | `letsencrypt` |
| acme_sh_account_email | **MANDATORY** The email of the account to request a certificate under. | |
| acme_sh_account_keyfile | File containing your account key for authentication with the ACME server | `"{{ acme_sh_home }}/ca_account.key"` |
| acme_sh_keylength | Specifies the domain key length: 2048, 3072, 4096, 8192 or ec-256, ec-384, ec-521. | `ec-384` |
| acme_sh_prehook | Pre hook that happens before attempting to issue a certificate | |
| acme_sh_post_hook | Post hook that happens after attempting to issue a certificate | |
| acme_sh_renew_hook | Renew hook that is called when certs are *successfully* renewed | |
| acme_sh_reloadcmd | Command run after newly renewed certificates are installed | |

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

Another way to consume this role would be:

```yaml
- name: Create Directory Tree Under ~
  hosts: servers
  gather_facts: false
  tasks:
    - name: Trigger invocation of run role
      ansible.builtin.include_role:
        name: marshallwp.general.acme_sh
      vars:
        acme_sh_mode: dns
        acme_sh_mode_value: dns_nsupdates
        acme_sh_dns_zone: _acme_challenge.example.com
        acme_sh_account_email: admin@example.com
```
