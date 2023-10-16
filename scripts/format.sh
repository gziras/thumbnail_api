#!/bin/sh -e
set -x

black src
ruff --fix src