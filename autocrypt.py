#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  autocrypt.py
#
#  Copyright 2023 Thomas Castleman <batcastle@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Auto-renew manually generated Let's Encrypt! SSL certs"""
from __future__ import print_function
import sys
import json
import datetime
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime
import os


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)


def get_certificate_expiry_date(certificate):
    """Find expiry date of cert"""
    cert = x509.load_pem_x509_certificate(certificate, default_backend())
    expiry_date = cert.not_valid_after
    return expiry_date


def convert_to_unix_time(expiry_date):
    """Convert `datetime` object to UNIX timestamp"""
    unix_time = expiry_date.timestamp()
    return unix_time


def get_current_unix_time():
    """get current time as UNIX timestamp"""
    return convert_to_unix_time(datetime.datetime.utcnow())


# load settings
with open("settings.json", "r") as file:
    SETTINGS = json.load(file)


# get domains to work on
DOMAINS = os.listdir(SETTINGS["PREFIX"])
DOMAINS.remove("README")
if SETTINGS["DOMAINS"] == []:
    ALLOWED_DOMAINS = DOMAINS
else:
    ALLOWED_DOMAINS = []
    for each in SETTINGS["DOMAINS"]:
        if each in DOMAINS:
            ALLOWED_DOMAINS.append(each)


# get cert files
CERTS = []
for each in ALLOWED_DOMAINS:
    if os.path.exists(each + "/fullchain.pem"):
        CERTS.append(each + "/fullchain.pem")


# read cert files
CERTS = {key: None for key in CERTS}
for each in CERTS.keys():
    with open(CERTS[each], "r") as file:
        CERTS[each] = file.read()


# get expiry times for each cert
for each in CERTS.keys():
    CERTS[each] = get_certificate_expiry_date(CERTS[each])
    #  CERTS[each] = convert_to_unix_time(CERTS[each])


# do something with this info
print(f"Current run time: { get_current_unix_time() }")
for each in CERTS.keys():
    print(f"Cert at { each } expires { CERTS[each] }, or { convert_to_unix_time(CERTS[each]) }")
