#!/bin/bash
WorkDir=`dirname $0`
cd ${WorkDir}
export PATH="/usr/local/miniconda3/bin/:$PATH"
python3.7 package.py
python3.7 main.py