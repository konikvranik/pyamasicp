#!/bin/bash
set -e -x

cd /io

apk add py3-pip

pip3 install build hatchling

# Build the wheel using hatchling
python3 -m build

# Fix the wheel using auditwheel for musllinux
auditwheel repair dist/*.whl -w /io/dist/ --plat musllinux_1_1_x86_64