#!/bin/bash
set -exv

BASE_IMG="quayio-update-ro-keys-job"

IMG="${BASE_IMG}:pr-check"

docker build -t "${IMG}" -f Dockerfile .
