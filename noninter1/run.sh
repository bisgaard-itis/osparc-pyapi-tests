#!/bin/bash

set -e

#rm -rf testenv
#python -m venv testenv
source ./testenv/bin/activate
# cp /home/vangeit/src/osparc-simcore-clients/clients/python/artifacts/dist/*.whl tmp_whl
# pip install pdb_attach
#pip install --force-reinstall /home/vangeit/src/osparc-simcore-clients/clients/python/artifacts/dist/*.whl
#pip install --extra-index-url=https://test.pypi.org/simple/ osparc==0.6.5.post10
#python -c 'import osparc; print(osparc.__version__)'
export OSPARC_DEV_FEATURES_ENABLED=1
rm -rf output_1
python -u run_study.py
