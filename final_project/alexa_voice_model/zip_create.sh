#!/bin/bash
zip -9 ./Deploy.zip
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 $VIRTUAL_ENV/Deploy.zip * 
cd $VIRTUAL_ENV/lib64/python2.7/site-packages
zip -r9 $VIRTUAL_ENV/Deploy.zip * 
cd $VIRTUAL_ENV/
zip -g Deploy.zip lambda_function.py
