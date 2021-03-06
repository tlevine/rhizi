#!/bin/bash
. src/local/utils.sh

if ! neo4j_running ; then
    $NEO4J_ROOT/bin/neo4j start
fi

CONFIG=res/etc/rhizi-server.conf
EXAMPLE=res/etc/rhizi-server.conf.example
HTPASSWD=res/etc/htpasswd
if [ "x$DOMAIN" == "x" ]; then
    echo using default domain
    DOMAIN=default.rhizi.net
else
    echo using $DOMAIN domain
fi
if [ ! -f $CONFIG ]; then
    echo "copying $EXAMPLE to $CONF"
    echo "please edit it as you see fit"
    cp $EXAMPLE $CONFIG
fi
make # building css relies on Makefile
ant -f build.ant deploy-local -DdefaultDomain=$DOMAIN -DtargetDomain=$DOMAIN && (
    mkdir -p deploy-local
    cd deploy-local
    python2.7 bin/rz_server.py --config-dir etc
)
