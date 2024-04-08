#!/bin/bash

set -ex

source ./testenv/bin/activate

pip install /home/vangeit/src/osparc-simcore-clients/clients/python/artifacts/dist/*.whl
rm -rf output_1
python run_study.py
