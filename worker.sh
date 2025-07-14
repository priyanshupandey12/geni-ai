#!/bin/bash

# export $(grep -v '^#' .env | xargs -d '\n') 
# rq worker --with-scheduler --url redis://valkey:6379

set -a                # Export all variables loaded
source .env           # Load the .env file
set +a                # Stop exporting automatically

rq worker --with-scheduler --url redis://valkey:6379