#!/bin/bash

REPO=$1
COMMIT=$2
source run_or_fail.sh
run_or_fail "Repo not found" pushd "$REPO"
run_or_fail "Could not clean repository" git clean -d -f -x
run_or_fail "Could not call git pull" git pull
run_or_fail "Could not update to given commit hash" git reset --hard "$COMMIT"
