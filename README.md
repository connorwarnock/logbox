# Logbox

## Setup
You will need to have Docker compose installed

Setup the .env file:

1. `cp .env.example .env`
2. Fill in your AWS `S3_KEY` and `S3_SECRET` values
3. Create a new `SECRET_KEY` - this can be any random string

Bring all of the containers up (this runs in the foreground until you hit ctrl-c):

    npm run up

With `npm run up` still going, setup the development and test databases

    npm run setup

### To ssh into a container

    npm run ssh

### Run the test suite(you will need to run `npm run up` and `npm run setup` first)

    npm test

While testing you may mess up the test database, and start getting database errors while running your tests.

Then you need to run `npm run setup` to reset the test database.

### Run the linter

    npm run lint

### Create a migration

    npm run migration -- -m create_logs

### Apply a migration

    npm run migrate

### Rollback a migration

    npm run rollback

### Connect to the database

    npm run db

### Generate an API token for a client
Supply a name for the client like `dumbledore`:

    npm run api-token -- mylittledrone

# Answers to additional considerations

## 1. Security
The app requires auth tokens in the header with every API request. All
requests are logged.

## 2. Scalability
We could scale horizontally with this system.  If database writes became
a bottleneck, we could stagger log ingestions or shard the database.
Using AWS lambda would also be advisable for log ingestion.

## 3. Integrity
We would implement hashes of all logs to verify proper upload from
drones.

Furthermore, every log would be saved in its original format in s3, replicated across
a geographically distinct zone. We could always compare hashes of the
logs in the db with the files to ensure consistency.  And if the db ever
disappeared, we could reload the log events from s3.

## 4. Testing
We'd aim for unit and request tests to ensure proper API responses. To
test capacity of the system, we'd simulate mass uploads with apache
benchmark or similiar scripts.
