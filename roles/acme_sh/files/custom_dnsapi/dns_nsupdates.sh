#!/bin/sh

# SPDX-FileCopyrightText: 2025 Industrial Info Resources, Inc.
# SPDX-FileContributor: William P. Marshall
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Custom variant of the built-in dns_nsupdate.sh script that supports
# cases where you must update multiple name-servers for every renewal.
#
# Usage is identical to that described in: https://github.com/acmesh-official/acme.sh/wiki/dnsapi#7-use-nsupdate-to-automatically-issue-cert
# Save that this script uses NSUPDATE_SERVERS (plural). The value of
# this variable is a comma-delimited list of nameservers.
#
# fulldomain is provided by acme.sh and is equivalent to the --domain-alias or --challenge-alias
# txtvalue is similarly provided by acme.sh.

#shellcheck disable=SC2034
dns_nsupdate_info='nsupdate RFC 2136 DynDNS client
Site: bind9.readthedocs.io/en/v9.18.19/manpages.html#nsupdate-dynamic-dns-update-utility
Docs: github.com/acmesh-official/acme.sh/wiki/dnsapi#dns_nsupdate
Options:
 NSUPDATE_SERVERS Server hostname(s). Default: "localhost".
 NSUPDATE_SERVER_PORT Server port. Default: "53".
 NSUPDATE_KEY File path to TSIG key.
 NSUPDATE_ZONE Domain zone to update. Optional.
'

########  Public functions #####################

#Usage: dns_nsupdates_add   _acme-challenge.www.domain.com   "XKrxpRBosdIKFzxW_CT3KLZNf6q0HG9i01zxXp5CPBs"
dns_nsupdates_add() {
  fulldomain=$1
  txtvalue=$2
  NSUPDATE_SERVERS="${NSUPDATE_SERVERS:-$(_readaccountconf_mutable NSUPDATE_SERVERS)}"
  NSUPDATE_SERVER_PORT="${NSUPDATE_SERVER_PORT:-$(_readaccountconf_mutable NSUPDATE_SERVER_PORT)}"
  NSUPDATE_KEY="${NSUPDATE_KEY:-$(_readaccountconf_mutable NSUPDATE_KEY)}"
  NSUPDATE_ZONE="${NSUPDATE_ZONE:-$(_readaccountconf_mutable NSUPDATE_ZONE)}"
  NSUPDATE_OPT="${NSUPDATE_OPT:-$(_readaccountconf_mutable NSUPDATE_OPT)}"

  _checkKeyFile || return 1

  # save the dns server and key to the account conf file.
  _saveaccountconf_mutable NSUPDATE_SERVERS "${NSUPDATE_SERVERS}"
  _saveaccountconf_mutable NSUPDATE_SERVER_PORT "${NSUPDATE_SERVER_PORT}"
  _saveaccountconf_mutable NSUPDATE_KEY "${NSUPDATE_KEY}"
  _saveaccountconf_mutable NSUPDATE_ZONE "${NSUPDATE_ZONE}"
  _saveaccountconf_mutable NSUPDATE_OPT "${NSUPDATE_OPT}"

  # Perform the update on each nameserver in the list.
  for NSUPDATE_SERVER in $(echo "$NSUPDATE_SERVERS" | sed 's/,/ /g')
  do
    [ -n "${NSUPDATE_SERVER}" ] || NSUPDATE_SERVER="localhost"
    [ -n "${NSUPDATE_SERVER_PORT}" ] || NSUPDATE_SERVER_PORT=53
    [ -n "${NSUPDATE_OPT}" ] || NSUPDATE_OPT=""

    _info "adding ${fulldomain}. 60 in txt \"${txtvalue}\""
    [ -n "$DEBUG" ] && [ "$DEBUG" -ge "$DEBUG_LEVEL_1" ] && nsdebug="-d"
    [ -n "$DEBUG" ] && [ "$DEBUG" -ge "$DEBUG_LEVEL_2" ] && nsdebug="-D"

    if [ -z "${NSUPDATE_ZONE}" ]; then
      #shellcheck disable=SC2086
      nsupdate -k "${NSUPDATE_KEY}" $nsdebug $NSUPDATE_OPT <<EOF
server ${NSUPDATE_SERVER}  ${NSUPDATE_SERVER_PORT}
update add ${fulldomain}. 60 in txt "${txtvalue}"
send
EOF
    else
      #shellcheck disable=SC2086
      nsupdate -k "${NSUPDATE_KEY}" $nsdebug $NSUPDATE_OPT <<EOF
server ${NSUPDATE_SERVER}  ${NSUPDATE_SERVER_PORT}
zone ${NSUPDATE_ZONE}.
update add ${fulldomain}. 60 in txt "${txtvalue}"
send
EOF
    fi
    #shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
      _err "error updating domain"
      return 1
    fi
  done

  return 0
}

#Usage: dns_nsupdates_rm   _acme-challenge.www.domain.com
dns_nsupdates_rm() {
  fulldomain=$1

  NSUPDATE_SERVERS="${NSUPDATE_SERVERS:-$(_readaccountconf_mutable NSUPDATE_SERVERS)}"
  NSUPDATE_SERVER_PORT="${NSUPDATE_SERVER_PORT:-$(_readaccountconf_mutable NSUPDATE_SERVER_PORT)}"
  NSUPDATE_KEY="${NSUPDATE_KEY:-$(_readaccountconf_mutable NSUPDATE_KEY)}"
  NSUPDATE_ZONE="${NSUPDATE_ZONE:-$(_readaccountconf_mutable NSUPDATE_ZONE)}"
  NSUPDATE_OPT="${NSUPDATE_OPT:-$(_readaccountconf_mutable NSUPDATE_OPT)}"

  # Perform the update on each nameserver in the list.
  for NSUPDATE_SERVER in $(echo "$NSUPDATE_SERVERS" | sed 's/,/ /g')
  do
    _checkKeyFile || return 1
    [ -n "${NSUPDATE_SERVER}" ] || NSUPDATE_SERVER="localhost"
    [ -n "${NSUPDATE_SERVER_PORT}" ] || NSUPDATE_SERVER_PORT=53
    _info "removing ${fulldomain}. txt"
    [ -n "$DEBUG" ] && [ "$DEBUG" -ge "$DEBUG_LEVEL_1" ] && nsdebug="-d"
    [ -n "$DEBUG" ] && [ "$DEBUG" -ge "$DEBUG_LEVEL_2" ] && nsdebug="-D"

    if [ -z "${NSUPDATE_ZONE}" ]; then
      #shellcheck disable=SC2086
      nsupdate -k "${NSUPDATE_KEY}" $nsdebug $NSUPDATE_OPT <<EOF
server ${NSUPDATE_SERVER}  ${NSUPDATE_SERVER_PORT}
update delete ${fulldomain}. txt
send
EOF
    else
      #shellcheck disable=SC2086
      nsupdate -k "${NSUPDATE_KEY}" $nsdebug $NSUPDATE_OPT <<EOF
server ${NSUPDATE_SERVER}  ${NSUPDATE_SERVER_PORT}
zone ${NSUPDATE_ZONE}.
update delete ${fulldomain}. txt
send
EOF
    fi
    #shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
      _err "error updating domain"
      return 1
    fi
  done

  return 0
}

####################  Private functions below ##################################

_checkKeyFile() {
  if [ -z "${NSUPDATE_KEY}" ]; then
    _err "you must specify a path to the nsupdate key file"
    return 1
  fi
  if [ ! -r "${NSUPDATE_KEY}" ]; then
    _err "key ${NSUPDATE_KEY} is unreadable"
    return 1
  fi
}
