#!/bin/bash
WorkDir=`dirname $0`
cd ${WorkDir}
python3.7 package.py
python3.7 main.py