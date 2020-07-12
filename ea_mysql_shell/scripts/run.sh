#!/bin/bash
set -e

MYSQL_USER=$( cat $MYSQL_USER )
MYSQL_PASSWORD=$( cat $MYSQL_PASSWORD )

echo $MYSQL_PASSWORD

if [ "$1" = 'mysqlsh' ]; then

    if [[ -z $MYSQL_HOST || -z $MYSQL_PORT || -z $MYSQL_USER || -z $MYSQL_PASSWORD ]]; then
	    echo "We require all of"
	    echo "    MYSQL_HOST"
	    echo "    MYSQL_PORT"
	    echo "    MYSQL_USER"
	    echo "    MYSQL_PASSWORD"
	    echo "to be set. Exiting."
	    exit 1
    fi
    max_tries=30
    attempt_num=0
    until (echo > "/dev/tcp/$MYSQL_HOST/$MYSQL_PORT") >/dev/null 2>&1; do
	    echo "Waiting for mysql server $MYSQL_HOST ($attempt_num/$max_tries)"
	    sleep 10
      	attempt_num=$(( attempt_num+1 ))
	    if (( attempt_num == max_tries )); then
		    exit 1
	    fi
    done
	until (echo > "/dev/tcp/$MYSQL_HOST2/$MYSQL_PORT2") >/dev/null 2>&1; do
	    echo "Waiting for mysql server $MYSQL_HOST2 ($attempt_num/$max_tries)"
	    sleep 10
      	attempt_num=$(( attempt_num+1 ))
	    if (( attempt_num == max_tries )); then
		    exit 1
	    fi
    done
	until (echo > "/dev/tcp/$MYSQL_HOST3/$MYSQL_PORT3") >/dev/null 2>&1; do
	    echo "Waiting for mysql server $MYSQL_HOST3 ($attempt_num/$max_tries)"
	    sleep 10
      	attempt_num=$(( attempt_num+1 ))
	    if (( attempt_num == max_tries )); then
		    exit 1
	    fi
    done
	echo "All Servers Ready"
	sleep 30
    if [ "$MYSQLSH_SCRIPT" ]; then
	mysqlsh "$MYSQL_USER@$MYSQL_HOST:$MYSQL_PORT" --dbpassword="$MYSQL_PASSWORD" -f "$MYSQLSH_SCRIPT" || true
    fi
    if [ "$MYSQL_SCRIPT" ]; then
	mysqlsh "$MYSQL_USER@$MYSQL_HOST:$MYSQL_PORT" --dbpassword="$MYSQL_PASSWORD" --sql -f "$MYSQL_SCRIPT" || true
    fi
	echo "Configuration Complete"
	sleep 3600
    exit 0
fi

exec "$@"
