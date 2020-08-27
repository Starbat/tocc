#!/bin/bash

PROJECTDIR=$(dirname $0)

cd ${PROJECTDIR}/src/main/python

python3 -m pytest
