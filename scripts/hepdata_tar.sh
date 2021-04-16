#!/bin/bash

name=''

if [ -z "$1" ]
then
    name=${PWD##*/}
else
    name=$1
fi

if [ -f "submission.yaml" ]
then
    echo Making a tar file for HEPData: $name.tar
    echo ---------------------------------------------------------
else
    echo The file submission.yaml not found, exiting
    exit -1
fi

if ls *.png 1> /dev/null 2>&1
then
    tar -cvf $name.tar *.yaml *.png
else
    tar -cvf $name.tar *.yaml
fi

