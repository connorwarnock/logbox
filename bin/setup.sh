#! /bin/sh

echo 'Creating development database...'

PGPASSWORD=password psql -h db -U postgres -c 'drop database if exists logbox'
PGPASSWORD=password psql -h db -U postgres -c 'create database logbox'

echo 'Running database migrations on development database...'

ENV=development alembic upgrade head

echo 'Creating test database...'

PGPASSWORD=password psql -h db -U postgres -c 'drop database if exists logbox_test'
PGPASSWORD=password psql -h db -U postgres -c 'create database logbox_test'

echo 'Running database migrations on test database...'

ENV=test alembic upgrade head
