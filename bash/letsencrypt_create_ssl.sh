#!/bin/bash
#
siteName=$1

[ -z $1 ] && (
    echo "Please input a arg(eg:$(basename $0) feelily-test.ivlii.com)"
    exit 1
)

certbot -d "${siteName}".com -d *."${siteName}".com --manual --preferred-challenges dns-01 --server https://acme-v02.api.letsencrypt.org/directory certonly
