#/usr/bin/bash

set -e

mongorestore -d sample_db mongodb://localhost:27017 /sample_collection.bson