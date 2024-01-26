#!/bin/bash

set -ex

source ./testenv/bin/activate

rm -rf output_1
python run_study.py
