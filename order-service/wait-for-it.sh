#!/bin/sh
host="$1"
port="$2"
shift 2

# skip until -- separator
while [ "$1" != "--" ]; do
  shift
done
shift # skip the '--'

# now "$@" là command cần chạy

until nc -z "$host" "$port"; do
  echo "Waiting for MySQL at $host:$port..."
  sleep 2
done

exec "$@"
